# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Entry script that is invoked by the driver script from automl."""
from typing import Any, Dict, Optional
from transformers import AutoTokenizer

import importlib
import logging
import numpy as np
import os

from azureml._common._error_definition import AzureMLError
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ExecutionFailure
from azureml.automl.core.shared.constants import Tasks
from azureml.automl.core.shared.exceptions import ValidationException
from azureml.automl.dnn.nlp.classification.io.read import dataloader
from azureml.automl.dnn.nlp.classification.multiclass.model_wrapper import ModelWrapper
from azureml.automl.dnn.nlp.classification.multiclass.trainer import TextClassificationTrainer
from azureml.automl.dnn.nlp.classification.multiclass.utils import compute_metrics
from azureml.automl.dnn.nlp.common._utils import (
    _get_language_code,
    create_unique_dir,
    is_data_labeling_run_with_file_dataset,
    prepare_run_properties,
    prepare_post_run_properties,
    save_script,
    save_conda_yml,
    scrub_system_exception,
    set_env_vars,
    is_main_process,
    save_deploy_script,
    _get_input_example_dictionary,
    _get_output_example,
    RootLoggingFilter
)
from azureml.automl.dnn.nlp.common.constants import (
    DataLiterals,
    OutputLiterals,
    ScoringLiterals,
    TaskNames,
    TrainingInputLiterals,
    SuppressedWarningPrefixes
)
from azureml.automl.dnn.nlp.common.io.utils import save_model_wrapper
from azureml.automl.dnn.nlp.common.training_configuration import TrainingConfiguration
from azureml.automl.runtime import _metrics_logging
from azureml.core.run import Run
from azureml.train.automl.runtime._code_generation.utilities import generate_nlp_code_and_notebook
from azureml.train.automl.runtime._entrypoints.utils.common import initialize_log_server

_logger = logging.getLogger(__name__)

horovod_spec = importlib.util.find_spec("horovod")
has_horovod = horovod_spec is not None


def run(
        automl_settings: Dict[str, Any],
        mltable_data_json: Optional[str] = None,
        **kwargs: Any
):
    """
    Invoke training by passing settings and write the output model.

    :param automl_settings: dictionary with automl settings
    :param mltable_data_json: mltable data json containing location of data
    """
    current_run = Run.get_context()
    try:
        workspace = current_run.experiment.workspace

        # Parse settings
        is_labeling_run = is_data_labeling_run_with_file_dataset(current_run)
        with RootLoggingFilter(SuppressedWarningPrefixes.ALL):
            automl_settings_obj = initialize_log_server(current_run, automl_settings)
        label_column_name = automl_settings_obj.label_column_name
        # Get primary metric
        primary_metric = automl_settings_obj.primary_metric
        # Get dataset language
        dataset_language = _get_language_code(automl_settings_obj.featurization)
        # Get enable distributed dnn training
        distributed = hasattr(automl_settings_obj, "enable_distributed_dnn_training") and \
            ((automl_settings_obj.enable_distributed_dnn_training is True)
             or (automl_settings_obj.enable_distributed_dnn_training == 'True')) and has_horovod
        # Get enable distributed dnn training for ORT and DeepSpeed
        distributed_ort_ds = hasattr(automl_settings_obj, "enable_distributed_dnn_training_ort_ds") and \
            ((automl_settings_obj.enable_distributed_dnn_training_ort_ds is True)
             or (automl_settings_obj.enable_distributed_dnn_training_ort_ds == 'True'))
        if distributed:
            _logger.info("horovod enabled: {}".format(distributed))
        elif distributed_ort_ds:
            _logger.info("ORT DS enabled: {}".format(distributed_ort_ds))

        # Get enable long range text: default value is True, but customers can disable this feature
        enable_long_range_text = automl_settings_obj.enable_long_range_text \
            if hasattr(automl_settings_obj, "enable_long_range_text") else True

        # Check label column and assign default label column for labeling run
        if label_column_name is None:
            if not is_labeling_run:
                raise ValidationException._with_error(
                    AzureMLError.create(
                        ExecutionFailure,
                        error_details="Need to pass in label_column_name argument for training"
                    )
                )
            label_column_name = DataLiterals.LABEL_COLUMN

        # Initialize Requirements
        # Data Directory
        data_dir = create_unique_dir(DataLiterals.DATA_DIR)
        # Load Training Config
        set_env_vars()
        training_configuration = TrainingConfiguration.populate_from_scope(task_type=Tasks.TEXT_CLASSIFICATION,
                                                                           dataset_language=dataset_language,
                                                                           automl_settings=automl_settings)
        # Get Tokenizer
        tokenizer = AutoTokenizer.from_pretrained(training_configuration[TrainingInputLiterals.TOKENIZER_NAME_OR_PATH],
                                                  use_fast=True)

        # Prepare Datasets
        training_set, validation_set, label_list, train_label_list, y_val = \
            dataloader.load_and_validate_multiclass_dataset(
                workspace=workspace, data_dir=data_dir, label_column_name=label_column_name,
                tokenizer=tokenizer, automl_settings=automl_settings, training_configuration=training_configuration,
                mltable_data_json=mltable_data_json, is_labeling_run=is_labeling_run,
                enable_long_range_text=enable_long_range_text
            )

        # Get trainer
        trainer_class = TextClassificationTrainer(train_label_list=train_label_list,
                                                  label_list=label_list,
                                                  training_configuration=training_configuration,
                                                  enable_distributed=distributed,
                                                  enable_distributed_ort_ds=distributed_ort_ds)
        prepare_run_properties(current_run, training_configuration[TrainingInputLiterals.MODEL_NAME])

        # Train
        trainer_class.train(training_set, validation_set)

        # Validate
        primary_metric_score = np.nan
        if validation_set is not None:
            val_predictions = trainer_class.validate(validation_set)
            if is_main_process():
                results = compute_metrics(y_val, val_predictions, label_list, train_label_list)
                primary_metric_score = results[primary_metric]
                log_binary = len(label_list) == 2
                _metrics_logging.log_metrics(current_run, results, log_binary=log_binary)

        # Save model artifacts
        if is_main_process():
            # Get input and output sample str
            input_sample_str = _get_input_example_dictionary(training_set.data,
                                                             label_column_name),
            output_sample_str = _get_output_example(training_set.data, label_column_name)
            # Save for inference
            if distributed_ort_ds:
                model_wrapper = ModelWrapper(trainer_class.model,
                                             label_list,
                                             tokenizer,
                                             training_configuration)
            else:
                model_wrapper = ModelWrapper(trainer_class.trainer.model,
                                             label_list,
                                             tokenizer,
                                             training_configuration)

            model_path = save_model_wrapper(run=current_run, model=model_wrapper,
                                            save_mlflow=automl_settings_obj.save_mlflow,
                                            input_sample_str=input_sample_str[0],
                                            output_sample_str=output_sample_str)
            multiclass_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                "io", "write", TaskNames.MULTICLASS)
            save_script(OutputLiterals.SCORE_SCRIPT, multiclass_directory)

            deploy_script_path = save_deploy_script(ScoringLiterals.MULTICLASS_SCORE_FILE,
                                                    input_sample_str[0],
                                                    output_sample_str)
            conda_file_path = save_conda_yml()

            # Update run
            # 2147483648 is 2 GB of memory
            prepare_post_run_properties(current_run,
                                        model_path,
                                        2147483648,
                                        conda_file_path,
                                        deploy_script_path,
                                        primary_metric,
                                        primary_metric_score)

            _logger.info("Code generation enabled: {}".format(automl_settings_obj.enable_code_generation))
            if automl_settings_obj.enable_code_generation:
                generate_nlp_code_and_notebook(current_run)
    except Exception as e:
        _logger.error("Multi-class runner script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(current_run, scrub_system_exception(e), update_run_properties=True)
        raise
