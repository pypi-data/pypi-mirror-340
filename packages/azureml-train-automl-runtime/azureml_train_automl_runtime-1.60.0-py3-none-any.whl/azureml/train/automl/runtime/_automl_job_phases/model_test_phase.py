# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import datetime
import numpy as np
import pandas as pd
from typing import Any, Optional, Union

from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.shared import constants
from azureml.automl.runtime._metrics_logging import log_metrics
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.shared.metrics_utilities import compute_metrics_expr_store, get_class_labels_expr_store
from azureml.automl.runtime.shared.model_wrappers import PipelineWithYTransformations
from azureml.core import Run
from azureml.train.automl.runtime._tsi import model_test_utilities
from azureml.automl.runtime.shared.score.scoring import aggregate_scores

logger = logging.getLogger(__name__)


class ModelTestPhase:
    """AutoML job phase that evaluates the model."""

    @staticmethod
    def run(
            model: Union[str, Any],
            test_run: Run,
            X_train: pd.DataFrame,
            y_train: np.ndarray,
            X_test: pd.DataFrame,
            y_test: Optional[np.ndarray],
            y_context: Optional[np.ndarray],
            label_column_name: str,
            task: str,
            is_timeseries: bool,
            positive_label: Optional[str] = None,
            enable_metric_confidence: bool = False,
            forecasting_aggregation_enabled: bool = False,
            test_include_predictions_only: bool = False) -> None:
        """
        Run the model test phase to calculate a set of metrics on a given model using a specific test dataset.

        :param model: The model to be tested. This should either be an MLFlow URI, or an in memory model that exposes
            predict, predict_proba, or forecast.
        :param test_run: The run context this phase is executing under.
        :param X_train: The original training dataset for this model.
        :param y_train: The original labels for this model.
        :param X_test: The test dataset to use to evaluate this model.
        :param y_test: The actual labels for the test dataset.
        :param y_context: The y context values for calculating forecast metrics.
        :param label_column_name: The name of the column containing the label.
        :param task: Classification or Regression
        :param is_timeseries: Flag whether this is a timeseries model.
        :param positive_label: class designed as positive class in binary classification metrics.
        :param enable_metric_confidence: Allow classfication metric calculation to include confidence intervals
            This is currently defaulted to False, and will have an automl config setting to enable
        :param test_include_predictions_only: Flag for whether to only include predictions in the test run.
        :return: None.
        """
        log_binary = False
        class_labels = None

        # Add extra logging to help diagnose issues with model testing.
        logger.info("ModelTestPhase: X_test.shape: {}".format(X_test.shape))
        if y_test is not None:
            logger.info("ModelTestPhase: y_test.type: {}".format(y_test.__class__.__name__))
        logger.info("ModelTestPhase: model type: {}".format(model.__class__.__name__))

        predict_start_time = datetime.datetime.utcnow()
        (y_pred, y_pred_values, X_forecast_transformed, y_test_transformed, y_pred_inv_transformed, _) = \
            model_test_utilities.inference(
                task=task,
                model=model,
                X_test=X_test,
                y_context=y_context,
                y_test=y_test,
                is_timeseries=is_timeseries)

        predict_time = datetime.datetime.utcnow() - predict_start_time

        if forecasting_aggregation_enabled \
                and not isinstance(model, str) \
                and hasattr(model, 'preaggregate_data_set'):
            _, y_test = model.preaggregate_data_set(X_test, y_test)

        if X_forecast_transformed is not None:
            # Use the transformed X_test which is returned from the
            # forecast method instead of the X_test from preaggregate_data_set
            # (above) since other non-aggregation transformations
            # (now or in the future) might have been done to X_test.
            X_test = X_forecast_transformed

        # Add extra logging to help diagnose issues with model testing.
        logger.info("ModelTestPhase: y_pred.shape: {}".format(y_pred.shape))
        predictions_output_df = model_test_utilities.get_output_dataframe(
            y_pred=y_pred,
            X_test=X_test,
            task_type=task,
            test_include_predictions_only=test_include_predictions_only,
            y_test=y_test,
            label_column_name=label_column_name,
            is_timeseries=is_timeseries
        )

        model_test_utilities._save_results(predictions_output_df, test_run)

        if y_test is not None:
            logger.info("Starting metrics computation for test run.")

            target_metrics = model_test_utilities.get_target_metrics(task, is_timeseries)
            confidence_metrics = None

            # The metrics computation for classification requires
            # the y_test values to be in encoded form.
            # also check if binary classification metrics should be logged
            if task == constants.Tasks.CLASSIFICATION:
                expr_store = ExperimentStore.get_instance()
                y_transformer = expr_store.transformers.get_y_transformer()
                confidence_metrics = constants.Metric.CLASSIFICATION_PRIMARY_SET
                if y_transformer:
                    y_test = y_transformer.transform(y_test)
                class_labels = get_class_labels_expr_store()  # further study decides switch to model.classes or not
                log_binary = len(class_labels) == 2 or positive_label is not None

            if isinstance(model, PipelineWithYTransformations):
                # Pass in the underlying pipeline so that the train labels
                # retrieval inside of compute_metrics gets the encoded labels.
                model = model.pipeline

            # Remove the rows which correspond to NaNs in
            # the predicted output before computing metrics.
            # See https://msdata.visualstudio.com/Vienna/_workitems/edit/1487484
            if len(y_pred_values.shape) == 1:
                row_mask = ~pd.isnull(y_pred_values)
            else:
                row_mask = ~(pd.isnull(y_pred_values).any(axis=1))

            num_nan_rows = np.count_nonzero(~row_mask)
            if num_nan_rows > 0:
                warning_msg = \
                    "{} out of {} rows contains NaNs in the predicted output. " \
                    "These rows will be dropped before metrics calculation." \
                    .format(num_nan_rows, len(row_mask))
                logger.warning(warning_msg)
                run_lifecycle_utilities.log_warning_message(test_run, warning_msg)

                X_test = X_test[row_mask]
                if y_test is not None:  # mypy complains without this check
                    y_test = y_test[row_mask]
                y_pred_values = y_pred_values[row_mask]

            # Add extra logging to help diagnose issues with model testing.
            logger.info("ModelTestPhase: X_test.shape: {}".format(X_test.shape))
            if y_test is not None:  # mypy complains without this check
                logger.info("ModelTestPhase: y_test.shape: {}".format(y_test.shape))
            logger.info("ModelTestPhase: y_pred_values.shape: {}".format(y_pred_values.shape))

            metrics = compute_metrics_expr_store(
                X_test=X_test,
                y_test=y_test,
                X_train=X_train,
                y_train=y_train,
                y_pred=y_pred_values,
                model=model,
                task=task,
                metrics=target_metrics,
                enable_metric_confidence=enable_metric_confidence,
                positive_label=positive_label,
                confidence_metrics=confidence_metrics,
                y_pred_original=y_pred_inv_transformed,
                y_test_original=y_test_transformed
            )

            # We need to aggregate scores to make sure that all data structures are
            # same as in CV scenario while training for forecasting.
            if task == constants.Tasks.FORECASTING or (task == constants.Tasks.REGRESSION and is_timeseries):
                metrics = aggregate_scores([metrics])

            # Add predict time to scores
            metrics[constants.TrainingResultsType.PREDICT_TIME] = predict_time.total_seconds()

            log_metrics(test_run, metrics, log_binary=log_binary)
        else:
            logger.info("Metrics computation skipped.")

        run_lifecycle_utilities.complete_run(test_run)
