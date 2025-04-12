# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Code gen related utility methods."""
from abc import ABC, abstractmethod
import inspect
import json
import logging
import os
import sys
from typing import Any, Dict, Optional, Tuple

from azureml._base_sdk_common._docstring_wrapper import module_logger as experimental_logger
from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import NotSupported
from azureml.core import Run
from azureml.core.script_run import ScriptRun
from azureml.training.tabular import VERSION

from azureml.automl.core import _codegen_utilities
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.constants import MLTableLiterals
from azureml.automl.core.shared.exceptions import ConfigException
from azureml.train.automl._constants_azureml import RunState
from azureml.train.automl.runtime import __version__
from azureml.train.automl.runtime._code_generation import code_generator, notebook_generator
from azureml.train.automl.runtime._code_generation.constants import CodeGenConstants

logger = logging.getLogger(__name__)


class CodeGeneratorType(ABC):
    """Code generator type base class"""

    @abstractmethod
    def generate_code(self, current_run: Run, pipeline: Optional[Any] = None) -> str:
        """Generate the script run code"""
        raise NotImplementedError

    @abstractmethod
    def generate_notebook(self, current_run: Run) -> Tuple[str, str, str]:
        """Generate the notebook that executes the script run code"""
        raise NotImplementedError


class TabularCodeGenerator(CodeGeneratorType):
    """TabularCodeGenerator"""

    def generate_code(self, current_run: Run, pipeline: Optional[Any] = None) -> str:
        """Generate the script run code for tabular data"""
        logger.info("Generating code for the trained model.")
        return code_generator.generate_full_script(current_run, pipeline)

    def generate_notebook(self, current_run: Run) -> Tuple[str, str, str]:
        """Generate the notebook that executes the script run code for tabular data"""
        notebook_file_name = CodeGenConstants.ScriptRunNotebookFilename
        notebook_output_path = CodeGenConstants.ScriptRunNotebookOutputPath

        if current_run.properties.get("run_algorithm") == 'TCNForecaster':
            parent_run = current_run.parent.parent
        else:
            parent_run = current_run.parent
        Contract.assert_value(parent_run, "parent")
        dataset_dict = get_input_datasets(parent_run)
        script_arguments = " ".join([f"--{k} {v}" for k, v in dataset_dict.items()])
        notebook_args = {
            'script_arguments': script_arguments,
            'training_package': f"azureml-train-automl~={__version__}"
        }
        notebook = notebook_generator.generate_script_run_notebook(
            current_run, parent_run=parent_run, template_name="script_run",
            environment=current_run.get_environment(), notebook_args=notebook_args)
        return notebook, notebook_file_name, notebook_output_path


class AutoFeaturizationCodeGenerator(CodeGeneratorType):
    """AutoFeaturizationCodeGenerator"""

    def generate_code(self, current_run: Run, pipeline: Optional[Any] = None) -> str:
        """Generate the script run code for the autofeaturization run"""
        logger.info("Generating code for Auto-featurization.")
        return code_generator.generate_autofeaturization_script(current_run, pipeline)

    def generate_notebook(self, current_run: Run) -> Tuple[str, str, str]:
        """Generate the notebook that executes the script run code"""
        notebook_file_name = CodeGenConstants.AutofeaturizationNotebookFilename
        notebook_output_path = CodeGenConstants.AutofeaturizationNotebookOutputPath

        try:
            env = Run(current_run.experiment, current_run.id + "_setup").get_environment()
        except Exception:
            env = None

        parent_run = current_run
        Contract.assert_value(parent_run, "parent")
        dataset_dict = get_input_datasets(parent_run)
        script_arguments = " ".join([f"--{k} {v}" for k, v in dataset_dict.items()])
        notebook_args = {
            'script_arguments': script_arguments,
            'training_package': f"azureml-train-automl~={__version__}",
        }
        notebook = notebook_generator.generate_script_run_notebook(
            current_run, parent_run=current_run, template_name="autofeaturization_run", environment=env,
            notebook_args=notebook_args
        )
        return notebook, notebook_file_name, notebook_output_path


class VerticalsCodeGenerator(CodeGeneratorType):
    def generate_code(self, current_run: Run, pipeline: Optional[Any] = None) -> str:
        """Generate the script run code for the NLP/Vision runs"""
        logger.info("Generating code.")
        return code_generator.generate_verticals_script()

    def generate_notebook(self, current_run: Run) -> Tuple[str, str, str]:
        """Generate the notebook that executes the script run code for NLP/Vision"""
        notebook_file_name = CodeGenConstants.ScriptRunNotebookFilename
        notebook_output_path = CodeGenConstants.ScriptRunNotebookOutputPath

        parent_run = current_run.parent.parent
        Contract.assert_value(parent_run, "parent")
        script_arguments = None
        if current_run.type == ScriptRun.RUN_TYPE:
            script_arguments = " ".join(sys.argv[1:])
        notebook_args = {'script_arguments': script_arguments}
        notebook = notebook_generator.generate_script_run_notebook(
            current_run, parent_run=parent_run, template_name="verticals_script_run",
            environment=current_run.get_environment(), compute_target_default="gpu-cluster",
            compute_sku=CodeGenConstants.VerticalsDefaultComputeSku, notebook_args=notebook_args)
        return notebook, notebook_file_name, notebook_output_path


def generate_autofeaturization_code_and_notebook(parent_run: Run, pipeline: Optional[Any] = None) -> None:
    try:
        generate_model_code_and_notebook(parent_run, pipeline, code_generator=AutoFeaturizationCodeGenerator())
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        logger.warning("Code generation failed for Auto-featurization; skipping.")


def generate_nlp_code_and_notebook(current_run: Run) -> None:
    try:
        generate_model_code_and_notebook(current_run, code_generator=VerticalsCodeGenerator())
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        logger.warning("Code generation failed for NLP; skipping.")


def generate_vision_code_and_notebook(current_run: Run) -> None:
    try:
        generate_model_code_and_notebook(current_run, code_generator=VerticalsCodeGenerator())
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        logger.warning("Code generation failed for Vision; skipping.")


def generate_model_code_and_notebook(current_run: Run, pipeline: Optional[Any] = None,
                                     code_generator: Optional[CodeGeneratorType] = None) -> None:
    """
    Given a child run, generate the code and notebook for the outputted model or autofeaturization run
    and upload them as artifacts. NOTE: parent run is the current run for autofeaturization
    """
    # Disable propagation for @experimental attribute during code gen because it can be noisy.
    should_propagate = experimental_logger.propagate
    try:
        experimental_logger.propagate = False

        if not code_generator:
            code_generator = TabularCodeGenerator()

        code = code_generator.generate_code(current_run, pipeline)
        with open(CodeGenConstants.ScriptFilename, "w") as f:
            f.write(code)
        current_run.upload_file(CodeGenConstants.ScriptOutputPath, CodeGenConstants.ScriptFilename)
        logger.info(f"Script has been generated, output saved to {CodeGenConstants.ScriptOutputPath}")

        try:
            # Quickly check for errors in the script
            _codegen_utilities.check_code_syntax(code)
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            logger.warning(
                "Code generation encountered an error when checking output. The generated code may "
                "require some manual editing to work properly."
            )

        try:
            notebook, notebook_file_name, notebook_output_path = code_generator.generate_notebook(current_run)
            with open(notebook_file_name, "w") as f:
                f.write(notebook)
            current_run.upload_file(notebook_output_path, notebook_file_name)

            logger.info(f"Notebook has been generated, output saved to {notebook_output_path}")
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            logger.warning(
                f"Notebook creation failed. Code Generator Type: {code_generator.__class__.__name__} "
            )

        current_run.set_tags({CodeGenConstants.TagName: RunState.COMPLETE_RUN})
    except ConfigException as e:
        logging_utilities.log_traceback(e, logger)
        logger.warning(f"Code generation not supported; skipping due to {e.message}.")
        current_run.set_tags({CodeGenConstants.TagName: RunState.CANCEL_RUN})
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        logger.warning("Code generation failed; skipping.")
        current_run.set_tags({CodeGenConstants.TagName: RunState.FAIL_RUN})
    finally:
        experimental_logger.propagate = should_propagate


def get_input_datasets(parent_run: Run) -> Dict[str, str]:
    """
    Given a parent run, fetch the IDs of the training and validation datasets, if present.

    :param parent_run: the run to fetch IDs from
    :return: a dict of training and validation dataset ID or URI to the value
    """
    parent_run_details = parent_run.get_details()
    input_datasets = parent_run_details.get("inputDatasets", [])
    dataset_dict = {}

    for input_dataset in input_datasets:
        consumption_block = input_dataset.get("consumptionDetails", {})
        dataset_name = consumption_block.get("inputName", None)

        if dataset_name == "training_data":
            dataset_dict['training_dataset_id'] = input_dataset["dataset"].id
        elif dataset_name == "validation_data":
            dataset_dict['validation_dataset_id'] = input_dataset["dataset"].id

    if 'training_dataset_id' not in dataset_dict:
        mltable_data_json = parent_run_details["properties"].get('mltable_data_json')
        if mltable_data_json:
            mltable_data = json.loads(mltable_data_json)
            train_data = mltable_data.get('TrainData', None)
            valid_data = mltable_data.get('ValidData', None)
            if train_data:
                dataset_dict['training_dataset_uri'] = train_data.get(MLTableLiterals.MLTABLE_RESOLVEDURI, None)
            if valid_data:
                dataset_dict['validation_dataset_uri'] = valid_data.get(MLTableLiterals.MLTABLE_RESOLVEDURI, None)
        if 'training_dataset_uri' not in dataset_dict:
            raise ConfigException._with_error(
                AzureMLError.create(
                    NotSupported, target="training_data", scenario_name="training_data_missing"
                )
            )

    return dataset_dict
