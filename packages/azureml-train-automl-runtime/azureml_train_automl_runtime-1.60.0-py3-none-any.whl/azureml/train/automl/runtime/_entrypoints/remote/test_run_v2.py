# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods for AutoML remote runs."""
import logging
from datetime import datetime
import mlflow
import numpy as np
import pandas as pd
from typing import Any, Optional

from azureml._tracing import get_tracer
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.shared import constants
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.telemetry_activity_logger import TelemetryActivityLogger
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.shared.memory_cache_store import MemoryCacheStore
from azureml.core import Run
from azureml.core.dataset import Dataset
from azureml.train.automl.run import AutoMLRun
from azureml.train.automl.runtime._automl_job_phases import ModelTestPhase
from azureml.train.automl.utilities import _get_package_version
from azureml.train.automl.runtime._tsi import model_test_utilities
from azureml.train.automl.runtime._entrypoints import entrypoint_util
from azureml.training.tabular.preprocessing.data_cleaning import _remove_nan_rows_in_X_y

logger = logging.getLogger(__name__)
activity_logger = TelemetryActivityLogger()
tracer = get_tracer(__name__)


def _set_expr_store(
        task,
        X_train,
        y_train,
        transformation_pipeline=None):
    # Create a new cache store for this TSI run
    expr_store = ExperimentStore(MemoryCacheStore(), read_only=False)
    expr_store.data.materialized.set_train(X_train, y_train, None)
    if task == "classification":
        expr_store.metadata.classification.class_labels = np.unique(y_train[~pd.isnull(y_train)])
        expr_store.metadata.classification.num_classes = len(expr_store.metadata.classification.class_labels)
    else:
        expr_store.metadata.regression.y_min = min(y_train)
        expr_store.metadata.regression.y_max = max(y_train)
        expr_store.metadata.regression.y_std = y_train.std()
        # bin info?
    expr_store.transformers.set_transformers({
        constants.Transformers.TIMESERIES_TRANSFORMER: transformation_pipeline
    })


def execute(
        script_directory: str,
        train_dataset: Optional[Dataset],
        test_dataset: Dataset,
        label_column_name: str,
        model_id: str,
        entry_point: str,
        y_transformer: Optional[Any] = None,
        transformation_pipeline: Optional[Any] = None,
        task: str = "classification",
        automl_run_id: Optional[str] = None,
        **kwargs: Any
) -> None:
    """
    Run the Model Test Phase to calculate metrics on a trained model using a test set.

    :param script_directory: Unused common parameter for phases.
    :param train_dataset: The original training dataset for this model.
    :param test_dataset: The test dataset to use to calculate metrics.
    :param label_column_name: The label column name for these datasets.
    :param model_id: The MLFlow model id for the model to be evaluated.
    :param entry_point: Unused common parameter for phases.
    :param y_transformer: The y_transformer to use for this phase. This is loaded from the cache store
        for AutoML runs.
    :param transformation_pipeline: The transformation pipeline for forecasting. This is loaded from the cache store
        for AutoML runs.
    :param task: What type of model is being evaluated: classification, regression, or forecasting.
    :param automl_run_id: The run id for an AutoML run. This is used to load the cache store.
    :param kwargs:
    :return:
    """
    current_run = Run.get_context()

    pkg_ver = _get_package_version()
    logger.info(f'Using SDK version {pkg_ver}')

    try:
        print(f"{datetime.now().__format__('%Y-%m-%d %H:%M:%S,%f')} - INFO - Beginning model test wrapper.")
        mlflow.set_tracking_uri(current_run.experiment.workspace.get_mlflow_tracking_uri())

        if automl_run_id:
            parent_run = AutoMLRun(current_run.experiment, automl_run_id)
            use_fd_cache = False
            for_distributed = False
            automl_settings_obj = parent_run._get_automl_settings()
            if hasattr(automl_settings_obj, "use_fd_cache"):
                use_fd_cache = True
            if getattr(automl_settings_obj, 'use_distributed', False):
                for_distributed = True
            cache_store = entrypoint_util.init_cache_store(parent_run,
                                                           use_fd_cache=use_fd_cache,
                                                           for_distributed=for_distributed)

            expr_store = ExperimentStore(cache_store, read_only=True)
            expr_store.load()
            X, y, _ = expr_store.data.materialized.get_train()
        else:
            Contract.assert_value(train_dataset, "train_dataset")
            X, y = model_test_utilities.get_X_y_from_dataset_label(train_dataset, label_column_name)
            _set_expr_store(
                task,
                X,
                y,
                transformation_pipeline)

        X_test, y_test = model_test_utilities.get_X_y_from_dataset_label(test_dataset, label_column_name)

        is_timeseries = False
        if task.lower() == "forecasting":
            task = "regression"
            is_timeseries = True

        # Clean X_test, y_test
        X_test, y_test, _ = _remove_nan_rows_in_X_y(
            X_test, y_test,
            is_timeseries=is_timeseries,
            target_column=label_column_name,
            featurization_config=automl_settings_obj.featurization
        )

        # y_context should be None for TSI
        y_context = None

        ModelTestPhase.run(
            model=model_id,
            test_run=current_run,
            X_train=X,
            y_train=y,
            X_test=X_test,
            y_test=y_test,
            y_context=y_context,
            label_column_name=label_column_name,
            task=task,
            is_timeseries=is_timeseries,
            test_include_predictions_only=False)
    except Exception as e:
        logger.error(f"AutoML test_wrapper script terminated with an exception of type: {type(e)}")
        run_lifecycle_utilities.fail_run(current_run, e)
        raise
    finally:
        ExperimentStore.reset()
