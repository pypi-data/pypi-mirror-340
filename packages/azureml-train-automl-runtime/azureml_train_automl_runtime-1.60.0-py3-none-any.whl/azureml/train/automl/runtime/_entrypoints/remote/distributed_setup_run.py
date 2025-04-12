# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Distributed setup run."""
import json
import logging
import os
from typing import Any, Optional, List, Dict

from azureml.automl.core.shared import logging_utilities
from azureml._common._error_definition import AzureMLError
from azureml._tracing import get_tracer
from azureml.automl.core._logging import log_server
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.dataset_utilities import get_datasets_from_data_json
from azureml.automl.core.shared._diagnostics.automl_error_definitions import \
    TimeseriesGrainAbsentValidateTrainValidData, TimeseriesGrainCountDifferenceBetweenTrainValid
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.constants import MLTableDataLabel
from azureml.automl.core.shared.exceptions import ConfigException
from azureml.automl.core.shared.forecasting_exception import ForecastingDataException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.telemetry_activity_logger import TelemetryActivityLogger
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.shared.lazy_azure_blob_cache_store import LazyAzureBlobCacheStore
from azureml.automl.core.shared._diagnostics.automl_error_definitions import NotSupported
from azureml.core import Run
from azureml.data import TabularDataset
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.runtime._automl_job_phases import \
    ForecastingDistributedFeaturizationPhase, ForecastingDistributedPreparationPhase, \
    ClassificationRegressionDistributedFeaturizationPhase, ForecastingPartitionPhase
from azureml.train.automl.runtime._automl_job_phases.distributed.classification_regression.preparation_phase import \
    ClassificationRegressionDistributedPreparationPhase
from azureml.train.automl.runtime._azureautomlruncontext import AzureAutoMLRunContext
from azureml.train.automl.runtime._entrypoints import entrypoint_util
from azureml.train.automl.runtime._automl_job_phases.distributed.experiment_state_plugin import ExperimentStatePlugin
from azureml.train.automl.runtime._partitioned_dataset_utils import \
    _get_sorted_partitions, _is_dataset_correctly_partitioned
from azureml.train.automl.runtime._worker_initiator import EXPERIMENT_STATE_PLUGIN
from dask.distributed import WorkerPlugin
from dask.distributed import get_client


logger = logging.getLogger(__name__)
activity_logger = TelemetryActivityLogger()
tracer = get_tracer(__name__)


class _LogInitializerWorkerPlugin(WorkerPlugin):
    """A worker plugin to initalize logging on dask workers for remote runs."""
    def __init__(self, run_id, automl_settings_str):
        self._run_id = run_id
        self._automl_settings_str = automl_settings_str

    def setup(self, worker):
        entrypoint_util.initialize_log_server(Run.get_context(), self._automl_settings_str)
        log_server.update_custom_dimension(pid=os.getpid())


def execute(
        script_directory: Optional[str],
        dataprep_json: str,
        automl_settings: str) -> None:

    setup_run = Run.get_context()
    workspace = setup_run.experiment.workspace

    try:
        with logging_utilities.log_activity(logger=logger, activity_name="Execution of distributed setup run"):

            verifier = VerifierManager()
            parent_run, automl_settings_obj, cache_store = entrypoint_util.init_wrapper(
                setup_run,
                automl_settings,
                script_directory
            )

            Contract.assert_type(value=cache_store, name='cache_store',
                                 expected_types=LazyAzureBlobCacheStore)

            expr_store = ExperimentStore(cache_store, read_only=False)
            dataprep_json_obj = json.loads(dataprep_json)

            training_dataset, validation_dataset, _ =\
                get_datasets_from_data_json(
                    workspace,
                    dataprep_json_obj,
                    [
                        MLTableDataLabel.TrainData,
                        MLTableDataLabel.ValidData
                    ]
                )
            assert training_dataset is not None

            # Save the raw dataset into expr_store
            expr_store.data.partitioned.save_raw_train_dataset(training_dataset)
            if validation_dataset is not None:
                expr_store.data.partitioned.save_raw_valid_dataset(validation_dataset)

            # register plug-ins required for dask
            logInitializerPlugin = _LogInitializerWorkerPlugin(setup_run.id,
                                                               automl_settings)
            get_client().register_worker_plugin(logInitializerPlugin)

            if automl_settings_obj.is_timeseries:
                _execute_for_forecasting(setup_run,
                                         parent_run.id,
                                         training_dataset,
                                         validation_dataset,
                                         automl_settings_obj,
                                         verifier,
                                         expr_store)
            else:
                _execute_for_classification_regression(setup_run,
                                                       parent_run.id,
                                                       training_dataset,
                                                       validation_dataset,
                                                       automl_settings_obj,
                                                       verifier,
                                                       expr_store)

            parent_run_context = AzureAutoMLRunContext(parent_run)
            verifier.write_result_file(parent_run_context)
            expr_store.unload()

    except Exception as e:
        logger.error("AutoML distributed setup script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(setup_run, e, update_run_properties=True)
        raise
    finally:
        # Reset the singleton for subsequent usage.
        ExperimentStore.reset()


def _execute_for_forecasting(setup_run: Run,
                             parent_run_id: str,
                             training_dataset: TabularDataset,
                             validation_dataset: Optional[TabularDataset],
                             automl_settings_obj: AzureAutoMLSettings,
                             verifier: VerifierManager,
                             expr_store: ExperimentStore) -> None:
    if not automl_settings_obj.grain_column_names:
        raise ConfigException._with_error(
            AzureMLError.create(
                NotSupported, scenario_name="missing_timeseries_ids"
            )
        )
    # this is a dirty work around. See 1484325
    automl_settings_obj.n_cross_validations = None
    training_dataset = _ensure_partitioned_if_exists(
        training_dataset,
        MLTableDataLabel.TrainData,
        parent_run_id,
        automl_settings_obj,
        expr_store,
    )
    validation_dataset = _ensure_partitioned_if_exists(
        validation_dataset,
        MLTableDataLabel.ValidData,
        parent_run_id,
        automl_settings_obj,
        expr_store,
    )

    logger.info("Fetching grain keys and values")
    original_grain_keyvalues_and_path = _get_sorted_partitions(training_dataset)
    original_grain_keyvalues = [grain_keyvalues_and_path.key_values
                                for grain_keyvalues_and_path in original_grain_keyvalues_and_path]

    original_grain_keyvalues_and_path_for_validation = []

    if validation_dataset:
        original_grain_keyvalues_and_path_for_validation = _get_sorted_partitions(validation_dataset)
        original_grain_keyvalues_for_validation = [grain_keyvalues_and_path.key_values
                                                   for grain_keyvalues_and_path
                                                   in original_grain_keyvalues_and_path_for_validation]

        _early_validate(original_grain_keyvalues, original_grain_keyvalues_for_validation)

    logger.info("total grains for the current experiment = {}".format(len(original_grain_keyvalues_and_path)))

    experiment_state_plugin = ExperimentStatePlugin(lambda: Run.get_context().experiment.workspace,
                                                    parent_run_id,
                                                    training_dataset,
                                                    validation_dataset,
                                                    automl_settings_obj)
    get_client().register_worker_plugin(experiment_state_plugin, EXPERIMENT_STATE_PLUGIN)

    ForecastingDistributedPreparationPhase.run(lambda: Run.get_context().experiment.workspace,
                                               Run.get_context().experiment.name,
                                               parent_run_id,
                                               automl_settings_obj,
                                               training_dataset,
                                               validation_dataset,
                                               original_grain_keyvalues_and_path,
                                               original_grain_keyvalues_and_path_for_validation,
                                               verifier)

    # We need to unload the experiment store to ensure it is
    # available in worker processes during the featurization phase.
    expr_store.unload()
    expr_store.load()

    # if data was prepared, use it, otherwise use training data.
    if expr_store.data.partitioned._prepared_train_dataset_id:
        prepared_train_data = expr_store.data.partitioned.get_prepared_train_dataset(setup_run.experiment.workspace)
        prepared_valid_data = expr_store.data.partitioned.get_prepared_valid_dataset(setup_run.experiment.workspace)
    else:
        prepared_train_data = training_dataset
        prepared_valid_data = validation_dataset

    prepared_grain_keyvalues_and_path = _get_sorted_partitions(prepared_train_data)
    prepared_grain_keyvalues_and_path_for_validation = _get_sorted_partitions(prepared_valid_data)

    ForecastingDistributedFeaturizationPhase.run(lambda: Run.get_context().experiment.workspace,
                                                 setup_run,
                                                 parent_run_id,
                                                 automl_settings_obj,
                                                 prepared_train_data,
                                                 prepared_valid_data,
                                                 original_grain_keyvalues,
                                                 prepared_grain_keyvalues_and_path,
                                                 prepared_grain_keyvalues_and_path_for_validation)


def _execute_for_classification_regression(setup_run: Run,
                                           parent_run_id: str,
                                           training_dataset: TabularDataset,
                                           validation_dataset: Optional[TabularDataset],
                                           automl_settings_obj: AzureAutoMLSettings,
                                           verifier: VerifierManager,
                                           expr_store: ExperimentStore) -> None:
    experiment_state_plugin = ExperimentStatePlugin(lambda: Run.get_context().experiment.workspace,
                                                    parent_run_id,
                                                    training_dataset,
                                                    validation_dataset,
                                                    automl_settings_obj)
    get_client().register_worker_plugin(experiment_state_plugin, EXPERIMENT_STATE_PLUGIN)

    ClassificationRegressionDistributedPreparationPhase.run(lambda: Run.get_context().experiment.workspace,
                                                            setup_run,
                                                            parent_run_id,
                                                            automl_settings_obj,
                                                            training_dataset,
                                                            validation_dataset)

    # We need to unload the experiment store to ensure it is
    # available in worker processes during the featurization phase.
    expr_store.unload()
    expr_store.load()

    # if data was prepared, use it, otherwise use training data.
    if expr_store.data.partitioned._prepared_train_dataset_id:
        prepared_train_data = expr_store.data.partitioned.\
            get_prepared_train_dataset(setup_run.experiment.workspace)
    else:
        prepared_train_data = training_dataset

    if expr_store.data.partitioned._prepared_valid_dataset_id:
        assert expr_store.data.partitioned._prepared_train_dataset_id
        prepared_valid_data = expr_store.data.partitioned. \
            get_prepared_valid_dataset(setup_run.experiment.workspace)
    else:
        prepared_valid_data = validation_dataset

    ClassificationRegressionDistributedFeaturizationPhase.run(lambda: Run.get_context().experiment.workspace,
                                                              setup_run,
                                                              parent_run_id,
                                                              automl_settings_obj,
                                                              prepared_train_data,
                                                              prepared_valid_data,
                                                              verifier)


def _early_validate(original_grain_keyvalues: List[Dict[str, Any]],
                    original_grain_keyvalues_for_validation: List[Dict[str, Any]]) -> None:

    if len(original_grain_keyvalues) != len(original_grain_keyvalues_for_validation):
        raise ForecastingDataException._with_error(
            AzureMLError.create(TimeseriesGrainCountDifferenceBetweenTrainValid, target='grain_difference',
                                reference_code=ReferenceCodes._TS_GRAIN_COUNT_MISMATCH,
                                training_grain_count=len(original_grain_keyvalues),
                                validation_grain_count=len(original_grain_keyvalues_for_validation)))

    # train and validation datasets must have same grain key values
    for t, v in zip(original_grain_keyvalues, original_grain_keyvalues_for_validation):
        if t != v:
            raise ForecastingDataException._with_error(
                AzureMLError.create(TimeseriesGrainAbsentValidateTrainValidData, target='grain_difference',
                                    reference_code=ReferenceCodes._TS_GRAIN_DIFFERENCE_EARLY_VALIDATE,
                                    grains=t,
                                    dataset_contain='training',
                                    dataset_not_contain='validation'))


def _ensure_partitioned_if_exists(
    dataset: Optional[TabularDataset],
    dataset_type: MLTableDataLabel,
    parent_run_id: str,
    automl_settings_obj: AzureAutoMLSettings,
    expr_store: ExperimentStore,
) -> Optional[TabularDataset]:
    """
    If the dataset is not None and not partitioned, partition it.

    :param dataset: The dataset to be partitioned if exists and not already partitioned.
    :param dataset_type: The type of the dataset.
    :param parent_run_id: The run id of the parent run.
    :param automl_settings_obj: The automl settings object.
    :param expr_store: The experiment store.

    :return: The partitioned dataset if dataset is not None.
    """
    if not _is_dataset_correctly_partitioned(dataset, automl_settings_obj.grain_column_names):
        ForecastingPartitionPhase.run(
            lambda: Run.get_context().experiment.workspace,
            parent_run_id,
            automl_settings_obj,
            dataset,
            dataset_type
        )
        return expr_store.data.partitioned.get_raw_partitioned_dataset(
            Run.get_context().experiment.workspace,
            dataset_type
        )
    return dataset
