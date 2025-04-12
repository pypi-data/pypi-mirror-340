# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This is the entry point into SDK for all remote runs"""

from typing import Any, Dict, List, Optional, cast
from azureml.automl.core.constants import PreparationRunTypeConstants
from azureml.core.dataset import Dataset
from azureml.train.automl.runtime._dask import DaskJob

from azureml.train.automl.runtime._entrypoints import local_managed_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_batch_training_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_explain_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_featurization_fit_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_featurization_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_setup_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_distributed_setup_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_test_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_test_run_entrypoint_v2
from azureml.train.automl.runtime._entrypoints import remote_training_run_entrypoint
from azureml.train.automl.runtime._entrypoints import hyperparameter_sweeping_run_entrypoint
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings


def setup_wrapper(
        script_directory: Optional[str],
        dataprep_json: str,
        entry_point: str,
        automl_settings: str,
        prep_type: str = PreparationRunTypeConstants.SETUP_ONLY,
        mltable_data_json: Optional[str] = None,
        **kwargs: Any
) -> None:
    """entry point for setup run"""
    # If MLTable data json is passed, use that instead of dataprep_json
    if dataprep_json is None and mltable_data_json:
        dataprep_json = mltable_data_json
    # this if condition is a stop-gap until we have better name for the flag and until we hae
    # jasmine changes for invoking distributed_setup_wrapper directly
    azure_automl_settings = AzureAutoMLSettings.from_string_or_dict(automl_settings)
    if getattr(azure_automl_settings, 'use_distributed', False):
        DaskJob.run(
            driver_func=remote_distributed_setup_run_entrypoint.execute,
            azure_automl_settings=azure_automl_settings,
            driver_func_args=[script_directory, dataprep_json, automl_settings],
        )
    else:
        remote_setup_run_entrypoint.execute(
            script_directory,
            dataprep_json,
            entry_point,
            automl_settings,
            prep_type,
            **kwargs)


def featurization_wrapper(
        script_directory: Optional[str],
        dataprep_json: str,
        entry_point: str,
        automl_settings: str,
        setup_container_id: str,
        featurization_json: str,
        mltable_data_json: Optional[str] = None,
        **kwargs: Any
) -> None:
    """entry point for featurization run"""
    if dataprep_json is None and mltable_data_json:
        dataprep_json = mltable_data_json
    remote_featurization_run_entrypoint.execute(
        script_directory,
        dataprep_json,
        entry_point,
        automl_settings,
        setup_container_id,
        featurization_json,
        ** kwargs)


def driver_wrapper(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        training_percent: float,
        iteration: int,
        pipeline_spec: str,
        pipeline_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> Dict[str, Any]:
    """entry point for training iteration run"""
    azure_automl_settings = AzureAutoMLSettings.from_string_or_dict(automl_settings)
    if getattr(azure_automl_settings, 'use_distributed', False):
        result = DaskJob.run(
            driver_func=remote_training_run_entrypoint.execute,
            azure_automl_settings=azure_automl_settings,
            driver_func_args=[script_directory, automl_settings, run_id, training_percent, iteration,
                              pipeline_spec, pipeline_id, dataprep_json, entry_point],
            driver_func_kwargs=kwargs,
            worker_per_core=False)
        return cast(Dict[str, Any], result)
    else:
        return remote_training_run_entrypoint.execute(
            script_directory,
            automl_settings,
            run_id,
            training_percent,
            iteration,
            pipeline_spec,
            pipeline_id,
            dataprep_json,
            entry_point,
            **kwargs)


def model_exp_wrapper(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        child_run_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> Dict[str, Any]:
    """entry point for expliner run"""
    return remote_explain_run_entrypoint.execute(
        script_directory,
        automl_settings,
        run_id,
        child_run_id,
        dataprep_json,
        entry_point,
        **kwargs)


def model_test_wrapper(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        training_run_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> None:
    """entry point for run that does inference and evaluation"""
    mltable_data_json = kwargs.get('mltable_data_json', None)
    if (dataprep_json is None or dataprep_json == "None") and mltable_data_json:
        dataprep_json = mltable_data_json
    remote_test_run_entrypoint.execute(
        script_directory,
        automl_settings,
        run_id,
        training_run_id,
        dataprep_json,
        entry_point,
        **kwargs)


def model_test_wrapper_v2(
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
    """entry point for run that does inference and evaluation"""
    remote_test_run_entrypoint_v2.execute(
        script_directory=script_directory,
        train_dataset=train_dataset,
        test_dataset=test_dataset,
        label_column_name=label_column_name,
        model_id=model_id,
        entry_point=entry_point,
        y_transformer=y_transformer,
        task=task,
        transformation_pipeline=transformation_pipeline,
        automl_run_id=automl_run_id,
        **kwargs)


def fit_featurizers_wrapper(
        script_directory: Optional[str],
        dataprep_json: str,
        entry_point: str,
        automl_settings: str,
        setup_container_id: str,
        featurization_json: str,
        **kwargs: Any
) -> None:
    """entry point for run that does fit on featurizer(s)"""
    mltable_data_json = kwargs.get('mltable_data_json', None)
    if (dataprep_json is None or dataprep_json == "None") and mltable_data_json:
        dataprep_json = mltable_data_json
    remote_featurization_fit_run_entrypoint.execute(
        script_directory,
        dataprep_json,
        entry_point,
        automl_settings,
        setup_container_id,
        featurization_json,
        ** kwargs)


def batch_driver_wrapper(
        script_directory: str,
        automl_settings: str,
        dataprep_json: str,
        child_run_ids: List[str],
        **kwargs: Any
) -> None:
    """entry point for run that does batch training iterations"""
    remote_batch_training_run_entrypoint.execute(
        script_directory,
        automl_settings,
        dataprep_json,
        child_run_ids,
        **kwargs)


def hyperparameter_sweeping_driver_wrapper(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        training_percent: float,
        iteration: int,
        pipeline_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> Dict[str, Any]:
    """entry point for training iteration run"""
    return hyperparameter_sweeping_run_entrypoint.execute(
        script_directory,
        automl_settings,
        run_id,
        training_percent,
        iteration,
        pipeline_id,
        dataprep_json,
        entry_point,
        **kwargs)


def local_managed_wrapper() -> None:
    local_managed_entrypoint.execute()
