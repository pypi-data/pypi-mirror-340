# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Dict, List, Optional
from azureml.automl.core.shared.constants import TimeSeriesInternal

from .node_columns_info import NodeColumnsInfo
from .hts_graph import Graph


class Arguments:
    """
    This class is used to hold the arguments that the AutoML PRS run needed.

    :param process_count_per_node: The number of processes per node.
    :param retrain_failed_models: Retrain the failed models.
    :param train_run_id: training run ID.
    :param target_column_name: The name of a target column.
    :param forecast_quantiles: The percentiles to be generated for the forecast.
    :param partition_column_names: The column names used to partition data set.
    :param hts_graph: hierarchical time series graph.
    :param output_path: The path to output files.
    :param target_path: The data store to be used to upload processed data.
    :param node_columns_info: the information about link between node id and columns in the data.
    :param input_metadata: The metadata on how the data set was aggregated to training level.
    :param engineered_explanation: If True, the engineering explanations will be generated.
    :param event_logger_dim: The dimensions to be logged.
    :param forecast_mode: The type of forecast to be used, either rolling or recursive, defaults to recursive.
    """

    def __init__(
            self,
            process_count_per_node: Optional[int] = None,
            retrain_failed_models: Optional[bool] = None,
            train_run_id: Optional[str] = None,
            target_column_name: Optional[str] = None,
            time_column_name: Optional[str] = None,
            forecast_quantiles: Optional[List[float]] = None,
            partition_column_names: Optional[List[str]] = None,
            hts_graph: Optional[Graph] = None,
            output_path: Optional[str] = None,
            target_path: Optional[str] = None,
            node_columns_info: Optional[Dict[str, NodeColumnsInfo]] = None,
            input_metadata: Optional[str] = None,
            engineered_explanation: Optional[bool] = None,
            event_logger_dim: Optional[Dict[str, str]] = None,
            enable_event_logger: Optional[bool] = False,
            inference_type: Optional[str] = None,
            forecast_mode: Optional[str] = TimeSeriesInternal.RECURSIVE,
            step: Optional[int] = 1,
            train_exp_name: Optional[str] = None,
            allow_multi_partitions: bool = False
    ) -> None:
        """
        This class is used to hold the arguments that the AutoML PRS run needed.

        :param process_count_per_node: The number of processes per node.
        :param retrain_failed_models: Retrain the failed models.
        :param train_run_id: training run ID.
        :param target_column_name: The name of a target column.
        :param forecast_quantiles: The percentiles to be generated for the forecast.
        :param partition_column_names: The column names used to partition data set.
        :param hts_graph: hierarchical time series graph.
        :param output_path: The path to output files.
        :param target_path: The data store to be used to upload processed data.
        :param node_columns_info: the information about link between node id and columns in the data.
        :param input_metadata: The metadata on how the data set was aggregated to training level.
        :param engineered_explanation: If True, the engineering explanations will be generated.
        :param event_logger_dim: The dimensions to be logged.
        :param inference_type: Which inference method to use on the model.
        :param forecast_mode: The type of forecast to be used, either rolling or recursive, defaults to recursive.
        :param step: Number of periods to advance the forecasting window in each iteration.
        """
        self.process_count_per_node = process_count_per_node
        self.retrain_failed_models = retrain_failed_models
        self.forecast_mode = forecast_mode
        self.step = step
        # used for MM inference.
        self.train_run_id = train_run_id
        self.target_column_name = target_column_name
        self.time_column_name = time_column_name
        self.forecast_quantiles = forecast_quantiles
        self.partition_column_names = partition_column_names
        self.inference_type = inference_type
        # used for HTS
        self.hts_graph = hts_graph
        self.output_path = output_path
        self.target_path = target_path
        self.event_logger_dim = event_logger_dim
        self.node_columns_info = node_columns_info
        self.input_metadata = input_metadata
        self.engineered_explanation = engineered_explanation
        self.enable_event_logger = enable_event_logger
        self.train_exp_name = train_exp_name
        self.allow_multi_partitions = allow_multi_partitions
