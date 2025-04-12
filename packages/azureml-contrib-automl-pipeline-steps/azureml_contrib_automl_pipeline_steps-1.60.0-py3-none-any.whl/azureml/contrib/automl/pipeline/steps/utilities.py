# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for interacting with AutoMLPipelineBuilder."""

from typing import Any, Dict, Optional, Tuple, Union
import logging
import os
import pathlib
import shutil

from azureml.core import ComputeTarget, Datastore, Environment, Experiment, Run, RunConfiguration, Workspace
from azureml._restclient.jasmine_client import JasmineClient
from azureml.pipeline.core import PipelineRun, PipelineData, StepRun
from azureml.data.output_dataset_config import OutputDatasetConfig
from azureml.train.automl.constants import Scenarios
from azureml.train.automl.constants import Tasks
from azureml.automl.core.shared.exceptions import ConflictingTimeoutException
from azureml.train.automl._hts import hts_client_utilities
from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ConflictingTimeoutError
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.train.automl._environment_utilities import (
    modify_run_configuration, get_curated_environment_label, get_curated_environment_scenario
)

logger = logging.getLogger(__name__)


def _validate_run_config_train(automl_settings: Dict[str, str],
                               compute,
                               node_count,
                               process_count_per_node,
                               run_invocation_timeout: int,  # in seconds
                               partition_column_names,
                               input_dataset):
    """
        Validation run config that is passed for training

        This method will validate the configuration to make sure we catch any errors before starting the run.

        :param automl_settings: AutoML configuration settings to be used for triggering AutoML runs during training.
        :param compute: The compute target name or compute target to be used by the pipeline's steps.
        :param node_count: The number of nodes to be used by the pipeline steps when work is
            distributable. This should be less than or equal to the max_nodes of the compute target
            if using amlcompute.
        :param process_count_per_node: The number of processes to use per node when the work is
            distributable. This should be less than or equal to the number of cores of the
            compute target.
        :param run_invocation_timeout: Specifies timeout for each AutoML run.
        :param partition_column_names: Column names which are used to partition the input data.
        :param input_dataset: The input dataset that is used.
    """

    experiment_timeout_hours = automl_settings.get('experiment_timeout_hours', 0)

    # PRS requires additional buffer to complete after experiment has completed or timed out
    if run_invocation_timeout < experiment_timeout_hours * 60 * 60 + 300:
        raise ConflictingTimeoutException._with_error(
            AzureMLError.create(
                ConflictingTimeoutError,
                reference_code=ReferenceCodes._VALIDATE_CONFLICTING_TIMEOUT,
                target='run_invocation_timeout'))


def get_step_run_env(
        automl_settings: Dict[str, Any],
        jasmine_client: JasmineClient,
        compute: Union[str, ComputeTarget],
        compute_sku: str,
        _workspace: Optional[Workspace] = None
) -> Environment:
    """
    Get the Environment for the pipeline steps.

    :param automl_settings: The AutoML settings dict.
    :param jasmine_client: The jasmine client to get the curated env.
    :param compute: The compute target.
    :param compute_sku: the name of the compute to be used.
    :param _workspace: Internal param for workspace to fetch envs if CE isn't released yet.
    :return: The curated environment based on the dnn and gpu settings.
    """
    enable_dnn = automl_settings.get("enable_dnn", False)
    # GPU based learners are currently available only for remote runs and so not available for many model runs
    enable_gpu = automl_settings.get("enable_gpu", False)
    task = Tasks.FORECASTING if automl_settings.get('is_timeseries') else automl_settings["task"]
    label = get_curated_environment_label(automl_settings)
    scenario = get_curated_environment_scenario(automl_settings, task)
    train_env = jasmine_client.get_curated_environment(
        scenario=scenario if scenario else Scenarios.AUTOML,
        enable_dnn=enable_dnn,
        enable_gpu=enable_gpu,
        compute=compute,
        compute_sku=compute_sku,
        label_override=label
    )
    return train_env


def get_default_inference_env(
        experiment: Experiment, train_run_id: str, train_experiment_name: str,
        step_name: str
) -> Environment:
    """Get the default inference env by giving train_run_id and train_experiment_name."""
    experiment = Experiment(experiment.workspace, train_experiment_name)
    pipeline_run = PipelineRun(experiment, train_run_id)
    step_run = pipeline_run.find_step_run(step_name)[0]
    inference_env = step_run.get_environment()
    return inference_env


def get_output_datastore_and_file(
        output: Union[OutputDatasetConfig, Datastore],
        output_name: str,
        pipeline_output_name: Optional[str] = None
) -> Tuple[Optional[Datastore], Union[OutputDatasetConfig, PipelineData]]:
    """
    Get the output datastore and the output data file location. If the input is data file,
    None will be returned as default datastore.

    :param output: The output location that will be used. It can either be a Datastore as a dir or an
        OutputDatasetConfig as a single file.
    :param output_name: The output name for the PipelineData.
    :param pipeline_output_name: The output name for the pipeline.
    :return: A tuple that contains output Datastore and the data file.
    """
    if isinstance(output, OutputDatasetConfig):
        # if outputdatasetconfig object is passed, pass on as is to PRS
        datastore = None
        output_file = output
    else:
        datastore = output
        output_file = PipelineData(
            name=output_name, datastore=datastore, pipeline_output_name=pipeline_output_name)

    return datastore, output_file


def get_module_file_abs_path(file_module: Any) -> pathlib.Path:
    """Get the absolute file path."""
    return pathlib.Path(file_module.__file__).absolute()


def get_output_from_mm_pipeline(
        run: Run,
        results_name: str,
        output_name: str,
        parallel_run_output_file_name: Optional[str] = None
) -> Optional[str]:
    """
    Get output data files from many models pipeline.

    **Note:** This method uses ``shutil.rmtree(results_name)`` which **deletes** the entire supplied directory tree.

    :param run: The run object for the run.
    :param results_name: The directory where the output file will be downloaded.
    :param output_name: The name of output, either 'many_models_inference_output' or
        'many_models_training_output' if not configured manually.
    :param parallel_run_output_file_name: The name of the parallel run output file
        (optional, default value is 'parallel_run_step.txt').
    :return: A string containing path to the downloaded output file or ``None`` in case of any error.
    """
    # remove previous run results, if present
    shutil.rmtree(results_name, ignore_errors=True)

    if parallel_run_output_file_name is None:
        parallel_run_output_file_name = "parallel_run_step.txt"
    result_file = None

    # download the contents of the output folder
    batch_runs = list(run.get_children())
    for batch_run in batch_runs:
        # only get output for the prs run.
        if batch_run.name in ('many-models-train', 'many-models-inference'):
            if not hasattr(batch_run, "get_output_data"):
                node_id = batch_run.properties.get("azureml.nodeid")
                batch_run = StepRun(batch_run.experiment, batch_run.id, run.id, node_id=node_id)
            batch_output = batch_run.get_output_data(output_name)
            batch_output.download(local_path=results_name)

            for root, dirs, files in os.walk(results_name):
                for file in files:
                    if file.endswith(parallel_run_output_file_name):
                        result_file = os.path.join(root, file)
                        break

    return result_file


def get_automl_environment(workspace: Workspace, automl_settings_dict: Dict[str, Any]) -> Environment:
    "Get the automl environment used for many models or hts."
    null_logger = logging.getLogger("null_logger")
    null_logger.addHandler(logging.NullHandler())
    null_logger.propagate = False
    automl_settings_obj = hts_client_utilities.get_automl_settings(automl_settings_dict)
    run_configuration = modify_run_configuration(
        automl_settings_obj,
        RunConfiguration(),
        logger=null_logger)

    return run_configuration.environment


def set_environment_variables_for_run(run_config: RunConfiguration):
    "Set environment variables on the run config for many models or hts runs"
    run_config.environment_variables['DISABLE_ENV_MISMATCH'] = True
    run_config.environment_variables['AUTOML_IGNORE_PACKAGE_VERSION_INCOMPATIBILITIES'] = 'True'
    run_config.environment_variables['AZUREML_FLUSH_INGEST_WAIT'] = ''
    run_config.environment_variables['AZUREML_OTEL_EXPORT_RH'] = ''
    # Batch / flush metrics in the many models scenario
    run_config.environment_variables["AZUREML_METRICS_POLLING_INTERVAL"] = '30'
