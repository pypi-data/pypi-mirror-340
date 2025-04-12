# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods for AutoML remote runs."""
import logging
from datetime import datetime
from typing import Any

from azureml.training.tabular.preprocessing.data_cleaning import _remove_nan_rows_in_X_y

from azureml._tracing import get_tracer
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.shared.constants import MLTableDataLabel
from azureml.automl.core.shared.telemetry_activity_logger import TelemetryActivityLogger
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.core import Run
from azureml.train.automl.runtime._automl_job_phases import ModelTestPhase
from azureml.train.automl.runtime._entrypoints import entrypoint_util
from azureml.train.automl.runtime._tsi import model_test_utilities
from azureml.train.automl.utilities import _get_package_version

logger = logging.getLogger(__name__)
activity_logger = TelemetryActivityLogger()
tracer = get_tracer(__name__)


def execute(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        training_run_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> None:
    """
    Compute best run or on-demand model testing in remote runs.

    :param script_directory:
    :param automl_settings:
    :param run_id: The run id for model test run.
    :param training_run_id: The id for the AutoML child run which contains the model.
    :param dataprep_json: The dataprep json which contains a reference to the test dataset.
    :param entry_point:
    :param kwargs:
    :return:
    """
    current_run = Run.get_context()

    pkg_ver = _get_package_version()
    logger.info('Using SDK version {}'.format(pkg_ver))

    try:
        print("{} - INFO - Beginning model test wrapper.".format(datetime.now().__format__('%Y-%m-%d %H:%M:%S,%f')))
        logger.info('Beginning AutoML remote driver for run {}.'.format(run_id))

        parent_run = entrypoint_util.get_parent_run(Run(current_run.experiment, training_run_id))
        automl_settings_obj = entrypoint_util.initialize_log_server(
            current_run, automl_settings, parent_run_id=parent_run.id)

        use_fd_cache = False
        for_distributed = False
        if hasattr(automl_settings_obj, "use_fd_cache"):
            use_fd_cache = True
        if getattr(automl_settings_obj, 'use_distributed', False):
            for_distributed = True

        # Get the post setup/featurization training data
        # which is required for metrics computation.
        cache_store = entrypoint_util.init_cache_store(parent_run,
                                                       use_fd_cache=use_fd_cache,
                                                       for_distributed=for_distributed)

        expr_store = ExperimentStore(cache_store, read_only=True)
        expr_store.load()

        if 'test_data' not in dataprep_json and MLTableDataLabel.TestData.value not in dataprep_json and \
                expr_store.data.partitioned._prepared_test_dataset_id:
            # this is not a on demand test run and this is a distributed training run
            test_dataset = expr_store.data.partitioned.get_prepared_test_dataset(current_run.experiment.workspace)
            test_df = test_dataset.to_pandas_dataframe()
            y_test = test_df[automl_settings_obj.label_column_name].values
            X_test = test_df.drop(columns=[automl_settings_obj.label_column_name])
        else:
            X_test, y_test = model_test_utilities.get_test_datasets_from_dataprep_json(
                current_run.experiment.workspace,
                dataprep_json,
                automl_settings_obj)

        task = automl_settings_obj.task_type
        fitted_model = model_test_utilities.get_model_from_training_run(current_run.experiment, training_run_id)

        # y_context should be None for TSI
        y_context = None

        # Clean X_test, y_test
        X_test, y_test, _ = _remove_nan_rows_in_X_y(
            X_test, y_test,
            is_timeseries=automl_settings_obj.is_timeseries,
            target_column=automl_settings_obj.label_column_name,
            featurization_config=automl_settings_obj.featurization
        )

        X, y, _ = expr_store.data.materialized.get_train()

        forecasting_aggregation_enabled = \
            automl_settings_obj.is_timeseries and \
            automl_settings_obj.target_aggregation_function is not None

        ModelTestPhase.run(
            model=fitted_model,
            test_run=current_run,
            X_train=X,
            y_train=y,
            X_test=X_test,
            y_test=y_test,
            y_context=y_context,
            label_column_name=automl_settings_obj.label_column_name,
            task=task,
            is_timeseries=automl_settings_obj.is_timeseries,
            enable_metric_confidence=automl_settings_obj.enable_metric_confidence,
            forecasting_aggregation_enabled=forecasting_aggregation_enabled,
            test_include_predictions_only=automl_settings_obj.test_include_predictions_only)
    except Exception as e:
        logger.error("AutoML test_wrapper script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(current_run, e)
        raise
    finally:
        ExperimentStore.reset()
