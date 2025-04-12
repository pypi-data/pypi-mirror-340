# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Dict, List, Any, Callable, Optional, Set, Tuple, cast
import copy
import gc
import logging
import os
import uuid
from azureml.automl.runtime.shared.problem_info import ProblemInfo

from azureml.data.abstract_dataset import _PartitionKeyValueCommonPath
from dask.distributed import WorkerPlugin
from dask.distributed import get_client, get_worker
from joblib import Parallel, delayed, parallel_backend
import pandas as pd

from azureml._common._error_definition import AzureMLError
from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core.constants import FeatureType
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    TimeseriesDfMultiFrequenciesDiffData,
    TimeseriesDsFreqLessThenFcFreq,
    TimeseriesDfFrequencyNotConsistent,
    TimeseriesInsufficientDataForAllGrains, TimeseriesInsufficientData)
from azureml.automl.core.shared.constants import (
    ShortSeriesHandlingValues,
    TimeSeries,
    TimeSeriesInternal,
    TimeSeriesWebLinks
)
from azureml.automl.core.shared.exceptions import DataException
from azureml.automl.core.shared.forecasting_exception import (
    ForecastingConfigException,
    ForecastingDataException)
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.types import GrainType
from azureml.automl.core.shared.utilities import get_min_points
from azureml.data import TabularDataset
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.runtime._automl_job_phases.utilities import PhaseUtil
from azureml.train.automl.runtime._worker_initiator import EXPERIMENT_STATE_PLUGIN, \
    STAT_CALCULATOR_PLUGIN
from azureml.train.automl.runtime._worker_initiator import get_worker_variables
from azureml.train.automl.runtime._partitioned_dataset_utils import (
    _get_dataset_for_grain,
    _to_dask_dataframe_of_random_grains,
    _get_partition_column_types
)

from azureml.automl.runtime import _data_transformation_utilities
from azureml.automl.runtime._freq_aggregator import _get_frequency_nanos
from azureml.automl.runtime._grain_preparer import _preprocess_grain, _validate_grain_by_dataset, GrainPreprocessResult
from azureml.automl.runtime._grain_stat_generator import _get_grain_stat, GrainStatistics
from azureml.automl.runtime.column_purpose_detection import _time_series_column_helper
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.featurizer.transformer.timeseries.forecasting_heuristic_utils import (
    try_get_auto_parameters
)
from azureml.automl.runtime.frequency_fixer import FREQUENCY_REJECT_TOLERANCE
from azureml.automl.runtime.stats_computation.raw_stats import TimeSeriesStat
from azureml.automl.runtime._time_series_data_set import TimeSeriesDataSet
from azureml.automl.runtime.featurizer.transformer.timeseries._distributed.distributed_timeseries_util import (
    convert_grain_dict_to_str)
from azureml.automl.runtime.featurizer.transformer.timeseries._validation._ts_tsdf_valid_worker import (
    TimeseriesDataFrameValidationWorker)


logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)

PREPROCESS_PLUGIN = 'preprocess_plugin'


class GrainStatCalculationPlugin(WorkerPlugin):
    def __init__(self, tsdf_freq_offset: pd.DateOffset):
        self.tsdf_freq_offset = tsdf_freq_offset


class PreProcessPlugin(WorkerPlugin):
    def __init__(self,
                 updated_featurization: FeaturizationConfig,
                 prepared_data_dir: str,
                 new_frequency: pd.DateOffset,
                 max_horizon: int,
                 min_points_per_grain: int,
                 should_aggregate: bool,
                 should_pad: bool,
                 should_perturb: bool):
        # These properties capture the common state required for pre-processing all grains
        # updated_featurization includes properties that are discovered such as column purposed which are eventually
        # overwritten on top of user provided auto-ml settings
        self.updated_featurization = updated_featurization
        self.prepared_data_dir = prepared_data_dir
        self.new_frequency = new_frequency
        self.max_horizon = max_horizon
        self.min_points_per_grain = min_points_per_grain
        self.should_aggregate = should_aggregate
        self.should_pad = should_pad
        self.should_perturb = should_perturb


class ForecastingDistributedPreparationPhase:
    """AutoML job phase that prepares the data."""

    @staticmethod
    def run(workspace_getter: Callable[..., Any],
            experiment_name: str,
            parent_run_id: str,
            automl_settings: AzureAutoMLSettings,
            training_dataset: TabularDataset,
            validation_dataset: Optional[TabularDataset],
            all_grain_keyvalues_and_path: List[_PartitionKeyValueCommonPath],
            all_grain_keyvalues_and_path_for_validation: Optional[List[_PartitionKeyValueCommonPath]],
            verifier: VerifierManager) -> None:
        """
        We do the following in this function
        We do grain statistics calculation in distributed way
        We do make some centralized decisions and stat summary calculations based on gathered statistics
        We do some centralized validations that cant be done in distributed way
        We then prepare data in distributed way (fixing frequency, aggregating and padding short series)
        We then invoke grain by grain validation in distributed way
        We then do train/valid split
        """

        PhaseUtil.log_with_memory("Beginning distributed preparation")
        client = get_client()

        with tracer.start_as_current_span(
            constants.TelemetryConstants.SPAN_FORMATTING.format(
                constants.TelemetryConstants.COMPONENT_NAME, constants.TelemetryConstants.DATA_PREPARATION
            ),
            user_facing_name=constants.TelemetryConstants.DATA_PREPARATION_USER_FACING
        ):
            logger.info("Getting auto params from subsample of data")
            tsdf_freq_offset, max_horizon, min_points_per_grain = get_auto_params_from_subsample(
                automl_settings,
                training_dataset,
                all_grain_keyvalues_and_path)

            grain_stats = None
            stat_calculator_plugin = GrainStatCalculationPlugin(tsdf_freq_offset)
            client.register_worker_plugin(stat_calculator_plugin, STAT_CALCULATOR_PLUGIN)
            with logging_utilities.log_activity(logger=logger, activity_name='DistributedGrainStatCalculation'):
                with parallel_backend('dask'):
                    grain_stats = Parallel(n_jobs=-1)(delayed(_get_grain_stat)(
                        grain_keyvalues_and_path,
                    ) for grain_keyvalues_and_path in all_grain_keyvalues_and_path)

            gc.collect()
            PhaseUtil.log_with_memory("Finished DistributedGrainStatCalculation")
            logger.info("Validating data based on grain statistics and calculating global stats")

            (
                new_frequency,
                should_aggregate,
                should_pad,
                global_series_start,
                global_series_end,
                all_long_grain_key_values_path,
                all_long_grain_key_values_path_for_validation,
                short_grain_key_values,
                filtered_grain_stats,
                should_perturb
            ) = validate_and_infer_global(
                automl_settings,
                grain_stats,
                min_points_per_grain,
                max_horizon,
                validation_dataset,
                all_grain_keyvalues_and_path,
                all_grain_keyvalues_and_path_for_validation
            )

            expr_store = ExperimentStore.get_instance()
            expr_store.metadata.timeseries.global_series_start = global_series_start
            expr_store.metadata.timeseries.global_series_end = global_series_end
            expr_store.metadata.timeseries.min_points_per_grain = min_points_per_grain
            expr_store.metadata.timeseries.short_grain_names = [
                convert_grain_dict_to_str(dt) for dt in short_grain_key_values]
            expr_store.metadata.task = constants.Tasks.FORECASTING
            # TimeSeriesStat will be used by TCN and need to be added to the problem info during featurization.
            series_lengths = [grain_stat.total_rows for grain_stat in grain_stats]
            series_stats = TimeSeriesStat(len(series_lengths))
            series_stats.set_stats(series_lengths)
            dataset_size_before_processing = sum(series_lengths)

            expr_store.metadata.timeseries.series_stats = series_stats

            # Build the snapshot of the data for X.
            subsampled_grains_ddf = _to_dask_dataframe_of_random_grains(training_dataset,
                                                                        all_grain_keyvalues_and_path,
                                                                        1)
            data_subset = subsampled_grains_ddf.compute()
            data_subset.drop(automl_settings.label_column_name, axis=1, inplace=True)
            expr_store.metadata.raw_data_snapshot_str = _data_transformation_utilities.get_data_snapshot(
                data_subset)

            prepared_data_dir = '{}_{}_prepared_{}'.format(experiment_name, parent_run_id, str(uuid.uuid4()))

            if validation_dataset is None:
                # We will make all_long_grain_key_values_path_for_validation
                # a list of Nones so it can be used in zip
                # statement below.
                all_long_grain_key_values_path_for_validation = [None] * len(all_long_grain_key_values_path)

            logger.info("Getting column purposes from subsample of data")
            set_column_purposes(automl_settings, training_dataset, all_long_grain_key_values_path)

            start_times = [grain_stat.start_time for grain_stat in filtered_grain_stats]

            preprocess_plugin = PreProcessPlugin(automl_settings.featurization,
                                                 prepared_data_dir,
                                                 new_frequency,
                                                 max_horizon,
                                                 min_points_per_grain,
                                                 should_aggregate,
                                                 should_pad,
                                                 should_perturb)
            client.register_worker_plugin(preprocess_plugin, PREPROCESS_PLUGIN)
            PhaseUtil.log_with_memory("Starting DistributedPreparation")
            with logging_utilities.log_activity(logger=logger, activity_name='DistributedPreparation'):
                with parallel_backend('dask'):
                    grain_preprocess_results = Parallel(n_jobs=-1)(delayed(_preprocess_one_grain)(
                        long_grain_key_values_path, long_grain_key_values_path_for_validation, start_time
                    ) for long_grain_key_values_path, long_grain_key_values_path_for_validation, start_time in zip(
                        all_long_grain_key_values_path,
                        all_long_grain_key_values_path_for_validation,
                        start_times))

            gc.collect()
            PhaseUtil.log_with_memory("Finished DistributedPreparation")

            dataset_size_after_processing = sum([g.num_of_rows for g in grain_preprocess_results])
            expr_store.metadata.problem_info = ProblemInfo(dataset_samples=dataset_size_after_processing)
            report_prepare_results(verifier, grain_preprocess_results,
                                   automl_settings,
                                   dataset_size_before_processing,
                                   dataset_size_after_processing,
                                   should_perturb)

            grain_column_types = _get_partition_column_types(all_grain_keyvalues_and_path)
            expr_store = ExperimentStore.get_instance()
            with logging_utilities.log_activity(logger=logger, activity_name='SavingPreparedTrainDataset'):
                expr_store.data.partitioned.save_prepared_train_dataset(
                    workspace_getter(),
                    prepared_data_dir + "/train",
                    training_dataset.partition_keys,
                    grain_column_types
                )

            with logging_utilities.log_activity(logger=logger, activity_name='SavingPreparedValidationDataset'):
                expr_store.data.partitioned.save_prepared_valid_dataset(
                    workspace_getter(),
                    prepared_data_dir + "/validation",
                    training_dataset.partition_keys,
                    grain_column_types
                )

    PhaseUtil.log_with_memory("Ending distributed preparation")


def set_column_purposes(automl_settings: AzureAutoMLSettings,
                        training_dataset: TabularDataset,
                        all_long_grain_key_values_path: List[_PartitionKeyValueCommonPath]) -> None:
    # Get aggregate column types using few grains and assume it is representative of the dataset.
    subsampled_grains_ddf = _to_dask_dataframe_of_random_grains(training_dataset, all_long_grain_key_values_path, 10)
    data_subset = subsampled_grains_ddf.compute()

    featurization_config = FeaturizationConfig()
    if isinstance(automl_settings.featurization, dict):
        # If user passed in a featurization config, update default with their configuration.
        featurization_config._from_dict(automl_settings.featurization)

    # These should be cached as StatsAndColumnPurpose
    numeric_columns = _time_series_column_helper.get_numeric_columns(
        data_subset, automl_settings.time_column_name,
        automl_settings.grain_column_names, featurization_config)  # type: Set[Any]
    datetime_columns = _time_series_column_helper.get_datetime_columns(
        data_subset, automl_settings.time_column_name,
        automl_settings.grain_column_names, featurization_config)  # type: Set[Any]

    current_purposes = featurization_config.column_purposes or {}

    for col in numeric_columns:
        if col not in current_purposes and col != automl_settings.label_column_name:
            current_purposes[col] = FeatureType.Numeric
    for col in datetime_columns:
        if col not in current_purposes:
            current_purposes[col] = FeatureType.DateTime

    featurization_config.column_purposes = current_purposes
    # TODO: make sure this is saved for featurization phase (and onward)
    # if aggregation is enabled for now we cannot persist this VSO: 1326498
    automl_settings.featurization = featurization_config.__dict__


def get_auto_params_from_subsample(automl_settings: AzureAutoMLSettings,
                                   training_dataset: TabularDataset,
                                   all_grain_keyvalues_and_path: List[_PartitionKeyValueCommonPath]
                                   ) -> Tuple[pd.DateOffset, int, int]:
    # In non-distributed runs frequency calculation on the tsds happens by
    # taking the mode frequency of the full tsds. Since we cannot do that with
    # distribution without an additional full pass on data, we subsample to 100
    # grains and then infer_freq on those.
    subsampled_grains_ddf = _to_dask_dataframe_of_random_grains(training_dataset, all_grain_keyvalues_and_path, 100)
    subsampled_X = subsampled_grains_ddf.compute()
    subsampled_Y = subsampled_X.pop(automl_settings.label_column_name).values

    tsds = TimeSeriesDataSet.create_tsds_safe(
        subsampled_X,
        subsampled_Y,
        target_column_name=automl_settings.label_column_name,
        time_column_name=automl_settings.time_column_name,
        origin_column_name=TimeSeriesInternal.ORIGIN_TIME_COLNAME_DEFAULT,
        grain_column_names=automl_settings.grain_column_names or [TimeSeriesInternal.DUMMY_GRAIN_COLUMN],
        boolean_column_names=None
    )

    tsds_freq_offset = tsds.infer_freq()

    # Compute auto parameters with subset of grains
    # For now we disable lags and rolling windows as FTCN
    # doesnt use these features
    _, _, max_horizon, _, _ = try_get_auto_parameters(
        automl_settings,
        subsampled_X,
        subsampled_Y,
        tsds_freq_offset
    )

    # If doing train/valid split ensure validation and training data is at least 1 full horizon.
    # We don't currently support CV so we pass none here.
    min_points_per_grain = get_min_points(0, [0], max_horizon, None)
    min_points_per_grain *= 2

    return tsds_freq_offset, max_horizon, min_points_per_grain


def _preprocess_one_grain(
    grain_keyvalues_and_path: _PartitionKeyValueCommonPath,
    grain_keyvalues_and_path_for_validation: Optional[_PartitionKeyValueCommonPath],
    start_time: pd.Timestamp
) -> GrainPreprocessResult:
    worker = get_worker()
    experiment_state_plugin = worker.plugins[EXPERIMENT_STATE_PLUGIN]
    preprocess_plugin = worker.plugins[PREPROCESS_PLUGIN]
    default_datastore_for_worker, workspace_for_worker, expr_store_for_worker = get_worker_variables(
        experiment_state_plugin.workspace_getter, experiment_state_plugin.parent_run_id)

    training_dataset_for_grain = _get_dataset_for_grain(grain_keyvalues_and_path,
                                                        experiment_state_plugin.training_dataset)
    os.makedirs(preprocess_plugin.prepared_data_dir, exist_ok=True)

    # load pandas dataframe for one grain
    train_X_grain = training_dataset_for_grain.to_pandas_dataframe()
    automl_settings_copy = copy.deepcopy(experiment_state_plugin.automl_settings)
    automl_settings_copy.featurization = preprocess_plugin.updated_featurization

    if grain_keyvalues_and_path_for_validation is not None:
        valid_X_grain = _get_dataset_for_grain(
            grain_keyvalues_and_path_for_validation,
            experiment_state_plugin.validation_dataset).to_pandas_dataframe()
    else:
        valid_X_grain = None
        # transform one grain
    train_prepared_data, validation_prepared_data, grain_preprocess_result = _preprocess_grain(
        train_X_grain,
        valid_X_grain,
        grain_keyvalues_and_path,
        preprocess_plugin.new_frequency,
        preprocess_plugin.max_horizon,
        start_time,
        preprocess_plugin.min_points_per_grain,
        automl_settings_copy,
        preprocess_plugin.should_aggregate,
        preprocess_plugin.should_pad,
        preprocess_plugin.should_perturb
    )

    for prepared_data, split in \
            zip([train_prepared_data, validation_prepared_data], ['train', 'validation']):
        # write one grain to local file
        # drop the grain columns since they will be part of the path and hence
        # they will be reconstructed as part of reading partitioned dataset
        prepared_data.reset_index(inplace=True, drop=True)
        prepared_data.drop(columns=experiment_state_plugin.automl_settings.grain_column_names, inplace=True)
        prepared_file_name = '{}-{}.parquet'.format(split, str(uuid.uuid4()))
        prepared_file_path = '{}/{}'.format(preprocess_plugin.prepared_data_dir, prepared_file_name)
        prepared_data.to_parquet(prepared_file_path)

        # construct the path to which data will be written to on the default blob store
        target_path_array = [preprocess_plugin.prepared_data_dir, split]
        for val in grain_keyvalues_and_path.key_values.values():
            target_path_array.append(str(val))
        target_path = '/'.join(target_path_array)

        # upload data to default store
        expr_store_for_worker.data.partitioned.write_file(prepared_file_path, target_path)
        logger.info("prepared one grain and uploaded data")

    return grain_preprocess_result


def validate_and_infer_global(
    automl_settings: AzureAutoMLSettings,
    grain_stats: List[GrainStatistics],
    min_points_per_grain: int,
    max_horizon: int,
    validation_data: Optional[TabularDataset],
    all_grain_keyvalues_and_path: List[_PartitionKeyValueCommonPath],
    all_grain_keyvalues_and_path_for_validation: Optional[List[_PartitionKeyValueCommonPath]]
) -> Tuple[pd.DateOffset, bool, bool, pd.Timestamp, pd.Timestamp,
           List[_PartitionKeyValueCommonPath], List[_PartitionKeyValueCommonPath],
           List[Dict[str, Any]], List[GrainStatistics], bool]:
    """
    This method is runs on driver node and is responsible for few things
    Validate global statistics -- such as all grains have same frequency
    Summarize global statistics
    Make global decisions such as following
        -- whether there is need to prepare data (either it is already good OR cant be fixed)
        -- what is common inferred frequency
    """
    should_pad = False
    should_drop = False
    should_aggregate = False
    should_perturb = all([g.n_unique_target == 1 for g in grain_stats])

    total_rows = sum([grain_stat.total_rows for grain_stat in grain_stats])
    TimeseriesDataFrameValidationWorker._check_tcn_min_points(None, total_rows, automl_settings)

    # Longest grain will be the longest set of non-null target values
    longest_grain = max([grain_stat.total_rows - grain_stat.n_null_target for grain_stat in grain_stats])

    frequencies_not_nan = {}  # type: Dict[pd.Timestamp, List[Dict[str, Any]]]
    for grain_stat in grain_stats:
        grain_id = grain_stat.grain_keys_values
        grain_freq = grain_stat.frequency

        if grain_freq in frequencies_not_nan:
            frequencies_not_nan[grain_freq].append(grain_id)
        else:
            frequencies_not_nan[grain_freq] = [grain_id]

    unique_freqs = frequencies_not_nan.keys()
    # If more than frequency is detected, set frequency to None and let subsequent flow determine frequency or raise
    new_frequency = list(unique_freqs)[0] if len(list(unique_freqs)) == 1 else None

    global_series_start = min([grain_stat.start_time for grain_stat in grain_stats])
    global_series_end = min([grain_stat.end_time for grain_stat in grain_stats])

    should_drop = automl_settings.short_series_handling_configuration == \
        ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
    if validation_data is None:
        should_pad = automl_settings.short_series_handling_configuration == \
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_PAD
        should_aggregate = automl_settings.target_aggregation_function is not None and automl_settings.freq is not None
        if automl_settings.short_series_handling_configuration == \
                ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO:
            if longest_grain < min_points_per_grain:
                should_pad = True
            else:
                should_drop = True

    # we now check that we at least do need one long grain.
    if should_drop and not should_pad and longest_grain < min_points_per_grain:
        raise ForecastingDataException._with_error(
            AzureMLError.create(TimeseriesInsufficientDataForAllGrains, target='X.shape',
                                reference_code=ReferenceCodes._TS_WRONG_SHAPE_DATA_FOR_ALL_GRAINS,
                                min_points=min_points_per_grain,
                                forecast_horizon=max_horizon)
        )

    if should_aggregate:
        if new_frequency is not None and (
            _get_frequency_nanos(automl_settings.freq) < _get_frequency_nanos(new_frequency)
        ):
            raise ForecastingConfigException._with_error(
                AzureMLError.create(
                    TimeseriesDsFreqLessThenFcFreq, target=TimeSeries.FREQUENCY,
                    reference_code=ReferenceCodes._FORECASTING_PARAM_USER_FREQ_DISTRIBUTED,
                    data_freq=new_frequency.freqstr,
                    forecast_freq=automl_settings.freq,
                    freq_doc=TimeSeriesWebLinks.FORECAST_PARAM_DOCS
                )
            )
    else:
        if len(unique_freqs) != 1:
            freqs_to_counts = {freq: len(grains) for freq, grains in frequencies_not_nan.items()}
            logger.error(f"Identified the following frequencies and corresponding grains: {freqs_to_counts}.")
            raise ForecastingDataException._with_error(
                AzureMLError.create(
                    TimeseriesDfMultiFrequenciesDiffData,
                    freq_counts_dict=freqs_to_counts,
                    freq_to_series_dict={freq: grains[0] for freq, grains in frequencies_not_nan.items()},
                    target='freq',
                    reference_code=ReferenceCodes._DIST_DATA_PREP_MULTI_FREQUENCIES_DIFF
                )
            )

        total_rows_in_coverage = sum(
            [grain_stat.total_rows_in_coverage for grain_stat in grain_stats
             if grain_stat.frequency is not None]
        )

        if total_rows_in_coverage / total_rows < FREQUENCY_REJECT_TOLERANCE:
            logging.error(
                f"Total rows covering current frequency: {total_rows_in_coverage}. Total rows in "
                f"data {total_rows}. {total_rows_in_coverage/total_rows} is below {FREQUENCY_REJECT_TOLERANCE}"
            )
            raise ForecastingDataException._with_error(
                AzureMLError.create(
                    TimeseriesDfFrequencyNotConsistent,
                    target='forecasting_parameters/freq',
                    reference_code=ReferenceCodes._DIST_DATA_PREP_INCONSISTENT_FREQUENCY,
                    freq=str(new_frequency),
                    forecasting_config=TimeSeriesWebLinks.FORECAST_CONFIG_DOC))

    long_grain_key_values_path = []
    long_grain_key_values_path_for_validation = []
    short_grain_key_values = []
    long_grain_stats = []
    detected_short_series = ''
    if should_drop:
        if not all_grain_keyvalues_and_path_for_validation:
            all_grain_keyvalues_and_path_for_validation = [None] * len(all_grain_keyvalues_and_path)

        pt_dict = {convert_grain_dict_to_str(gs.grain_keys_values): gs for gs in grain_stats}
        for grain_keyvalues_and_path, grain_keyvalues_and_path_for_validation \
                in zip(all_grain_keyvalues_and_path, all_grain_keyvalues_and_path_for_validation):
            g_key = convert_grain_dict_to_str(grain_keyvalues_and_path.key_values)
            if pt_dict[g_key].total_rows >= min_points_per_grain:
                long_grain_stats.append(pt_dict[g_key])
                long_grain_key_values_path.append(grain_keyvalues_and_path)
                long_grain_key_values_path_for_validation.append(grain_keyvalues_and_path_for_validation)
            else:
                short_grain_key_values.append(grain_keyvalues_and_path.key_values)
        detected_short_series = (
            f'\nThe data set contains {len(long_grain_key_values_path)} long and '
            f'{len(short_grain_key_values)} short series.')
    else:
        # If we are not dropping any grains, we are considering all grains to be long.
        long_grain_key_values_path = all_grain_keyvalues_and_path
        if all_grain_keyvalues_and_path_for_validation:
            long_grain_key_values_path_for_validation = all_grain_keyvalues_and_path_for_validation
        long_grain_stats = grain_stats

    logger.info(
        "The following settings have been identified:"
        "\n\tnew_frequency: {}\n\tshould_aggregate: {}\n\tshould_pad: {}\n\tshould_drop: {}{}"
        .format(new_frequency, should_aggregate, should_pad, should_drop, detected_short_series)
    )

    return (new_frequency, should_aggregate, should_pad, global_series_start,
            global_series_end, long_grain_key_values_path, long_grain_key_values_path_for_validation,
            short_grain_key_values, long_grain_stats, should_perturb)


def report_prepare_results(verifier: VerifierManager,
                           grain_preprocess_results: List[GrainPreprocessResult],
                           automl_settings: AzureAutoMLSettings,
                           dataset_size_before_processing: int,
                           dataset_size_after_processing: int,
                           should_perturb: bool) -> None:
    grains_padded = [g.name for g in filter(lambda x: x.is_padded, grain_preprocess_results)]
    grains_aggregated = [g.name for g in filter(lambda x: x.is_aggregated, grain_preprocess_results)]
    grains_freq_fixed = [g.name for g in filter(lambda x: x.is_frequency_fixed, grain_preprocess_results)]
    grains_drop_unique = [g.name for g in filter(lambda x: x.is_drop_unique, grain_preprocess_results)]

    logger.info(
        "Preprocessing results for all grains:"
        "\n\tgrains_padded: {}\n\tgrains_aggregated: {}\n\tgrains_freq_fixed: {}"
        .format(len(grains_padded), len(grains_aggregated), len(grains_freq_fixed))
    )

    verifier.update_data_verifier_aggregation(len(grains_aggregated) > 0,
                                              automl_settings.target_aggregation_function,
                                              automl_settings.freq)
    verifier.update_data_verifier_frequency_inference(False, len(grains_freq_fixed) > 0)
    verifier.update_data_verifier_short_grain_handling(grains_padded, [])
    verifier.update_data_verifier_insufficient_data_forecast_tcn(dataset_size_before_processing,
                                                                 dataset_size_after_processing,
                                                                 len(grain_preprocess_results) > 1,
                                                                 automl_settings.enable_dnn)
    if should_perturb:
        verifier.update_data_verifier_for_unique_target_grains(is_all_grains_unique_target=True)
    else:
        verifier.update_data_verifier_for_unique_target_grains(grains_drop_unique)
