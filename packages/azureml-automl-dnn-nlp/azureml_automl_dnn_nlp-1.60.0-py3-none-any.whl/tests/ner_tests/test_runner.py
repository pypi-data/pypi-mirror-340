from unittest.mock import MagicMock, Mock, patch

import unittest
import pytest

from azureml.automl.core.shared.exceptions import ClientException, DataException
from azureml.automl.dnn.nlp.common._diagnostics.nlp_error_definitions import AutoNLPInternal
from azureml.automl.dnn.nlp.common.constants import ModelNames
from azureml.automl.dnn.nlp.ner import runner
from ..mocks import (
    aml_label_dataset_mock,
    file_dataset_mock,
    get_ner_labeling_df,
    MockRun,
    ner_trainer_mock,
    open_ner_file,
    MockValidator
)


@patch("azureml.automl.dnn.nlp.common.training_configuration.ResourcePathResolver",
       return_value=Mock(model_name=ModelNames.BERT_BASE_CASED, model_path="some_path", tokenizer_path="some_path"))
@pytest.mark.usefixtures('new_clean_dir')
class NERRunnerTests(unittest.TestCase):
    """Tests for NER trainer."""

    @patch("azureml.automl.dnn.nlp.ner.trainer.Trainer")
    @patch("azureml.automl.dnn.nlp.ner.trainer.AutoConfig.from_pretrained")
    @patch("azureml.automl.dnn.nlp.ner.trainer.AutoModelForTokenClassification.from_pretrained")
    @patch("azureml.core.Dataset.get_by_id")
    @patch("azureml.automl.dnn.nlp.ner.runner.create_unique_dir")
    @patch("azureml.automl.dnn.nlp.ner.runner.initialize_log_server")
    @patch("azureml.automl.dnn.nlp.ner.runner.save_model_wrapper")
    @patch("azureml.automl.dnn.nlp.ner.runner.save_conda_yml")
    @patch("azureml.automl.dnn.nlp.ner.runner.AutoTokenizer.from_pretrained")
    @patch("azureml.automl.dnn.nlp.ner.runner.prepare_post_run_properties")
    @patch("azureml.automl.dnn.nlp.ner.runner.Run")
    @patch("azureml.automl.dnn.nlp.ner.io.read.dataloader.NLPNERDataValidator")
    def test_runner(
            self,
            validator_mock,
            run_mock,
            post_run_mock,
            tokenizer_factory_mock,
            conda_yml_mock,
            save_model_mock,
            initialize_log_server_mock,
            unique_dir_mock,
            get_by_id_mock,
            model_factory_mock,
            config_factory_mock,
            trainer_mock,
            path_resolver_mock
    ):
        # run mock
        mock_run = MockRun()
        run_mock.get_context.return_value = mock_run

        # settings mock
        automl_settings = {
            "task_type": "text-ner",
            "primary_metric": "accuracy",
            "dataset_id": "mock_dataset_id",
            "validation_dataset_id": "mock_validation_dataset_id"
        }
        mock_settings = MagicMock()
        mock_settings.dataset_id = "mock_dataset_id"
        mock_settings.validation_dataset_id = "mock_validation_dataset_id"
        mock_settings.primary_metric = "accuracy"
        mock_settings.save_mlflow = True
        mock_settings.enable_code_generation = True
        initialize_log_server_mock.return_value = mock_settings
        unique_dir_mock.return_value = "ner_data"

        # Get and validate dataset mocks
        get_by_id_mock.return_value = file_dataset_mock()
        validator_mock.return_value = MockValidator()

        mock_trainer = ner_trainer_mock()
        trainer_mock.return_value = mock_trainer

        # Test runner
        runner.run(automl_settings)

        # Asserts
        mock_trainer.train.assert_called_once()
        mock_trainer.save_model.assert_called_once()
        mock_trainer.save_state.assert_called_once()
        self.assertEqual(model_factory_mock.call_args[0][0], "some_path")

    @patch("azureml.automl.dnn.nlp.ner.trainer.Trainer")
    @patch("azureml.automl.dnn.nlp.ner.trainer.AutoConfig.from_pretrained")
    @patch("azureml.automl.dnn.nlp.ner.trainer.AutoModelForTokenClassification.from_pretrained")
    @patch("azureml.automl.dnn.nlp.ner.io.read.dataloader.copyfile")
    @patch("azureml.core.Dataset.get_by_id")
    @patch("azureml.automl.dnn.nlp.ner.runner.initialize_log_server")
    @patch("azureml.automl.dnn.nlp.ner.runner.save_model_wrapper")
    @patch("azureml.automl.dnn.nlp.ner.runner.save_conda_yml")
    @patch("azureml.automl.dnn.nlp.ner.runner.AutoTokenizer.from_pretrained")
    @patch("azureml.automl.dnn.nlp.ner.runner.prepare_post_run_properties")
    @patch("azureml.automl.dnn.nlp.ner.runner.Run.get_context")
    @patch("azureml.automl.dnn.nlp.ner.io.read.dataloader.NLPNERDataValidator")
    def test_runner_labeling_service(
            self,
            validator_mock,
            run_mock,
            post_run_mock,
            tokenizer_factory_mock,
            conda_yml_mock,
            save_model_mock,
            initialize_log_server_mock,
            get_by_id_mock,
            copyfile_mock,
            model_factory_mock,
            config_factory_mock,
            trainer_mock,
            path_resolver_mock
    ):

        # tokenizer mock
        tokenizer = MagicMock()
        tokenizer.model_max_length = 128
        tokenizer_factory_mock.return_value = tokenizer

        # run mock
        mock_run = MockRun(
            run_source="Labeling"
        )
        run_mock.return_value = mock_run

        # settings mock
        automl_settings = {
            "task_type": "text-ner",
            "primary_metric": "accuracy",
            "dataset_id": "mock_dataset_id",
            "validation_dataset_id": "mock_validation_dataset_id"
        }
        mock_settings = MagicMock()
        mock_settings.dataset_id = "mock_dataset_id"
        mock_settings.validation_dataset_id = "mock_validation_dataset_id"
        mock_settings.primary_metric = "accuracy"
        mock_settings.save_mlflow = True
        initialize_log_server_mock.return_value = mock_settings

        # Load and validate dataset mocks
        get_by_id_mock.return_value = aml_label_dataset_mock('TextNamedEntityRecognition',
                                                             data_df=get_ner_labeling_df())
        validator_mock.return_value = MockValidator()

        # Trainer mock
        mock_trainer = ner_trainer_mock()
        trainer_mock.return_value = mock_trainer

        # Test runner
        open_mock = MagicMock(side_effect=open_ner_file)
        with patch("builtins.open", new=open_mock):
            runner.run(automl_settings)

        # Asserts
        mock_trainer.train.assert_called_once()
        mock_trainer.save_model.assert_called_once()
        mock_trainer.save_state.assert_called_once()

    @patch("azureml.automl.dnn.nlp.ner.runner.AutoTokenizer.from_pretrained")
    @patch("azureml.core.Dataset.get_by_id")
    @patch("azureml.automl.dnn.nlp.ner.runner.initialize_log_server")
    @patch("azureml.automl.dnn.nlp.ner.runner.Run")
    @patch("azureml.automl.dnn.nlp.ner.io.read.dataloader.NLPNERDataValidator")
    def test_runner_without_validation_data(
            self,
            validator_mock,
            run_mock,
            initialize_log_server_mock,
            get_by_id_mock,
            tokenizer_factory_mock,
            path_resolver_mock
    ):
        # run mock
        mock_run = MockRun()
        run_mock.get_context.return_value = mock_run

        # settings mock
        automl_settings = {
            "task_type": "text-ner",
            "primary_metric": "accuracy",
            "dataset_id": "mock_dataset_id",
            "validation_dataset_id": None
        }
        mock_settings = MagicMock()
        mock_settings.dataset_id = "mock_dataset_id"
        mock_settings.validation_dataset_id = None
        mock_settings.primary_metric = "accuracy"
        mock_settings.save_mlflow = True
        initialize_log_server_mock.return_value = mock_settings

        # dataset get_by_id mock
        get_by_id_mock.return_value = file_dataset_mock()

        # data validation mock
        validator_mock.return_value = MockValidator()

        # Test runner
        with self.assertRaises(DataException):
            runner.run(automl_settings)

    @patch("azureml.automl.dnn.nlp.ner.trainer.Trainer")
    @patch("azureml.automl.dnn.nlp.ner.trainer.AutoConfig.from_pretrained")
    @patch("azureml.automl.dnn.nlp.ner.trainer.AutoModelForTokenClassification.from_pretrained")
    @patch("azureml.automl.dnn.nlp.ner.runner.AutoTokenizer.from_pretrained")
    @patch("azureml.data.abstract_dataset.AbstractDataset._load")
    @patch("azureml.automl.dnn.nlp.ner.runner.create_unique_dir")
    @patch("azureml.automl.dnn.nlp.ner.runner.initialize_log_server")
    @patch("azureml.automl.dnn.nlp.ner.runner.save_model_wrapper")
    @patch("azureml.automl.dnn.nlp.ner.runner.save_conda_yml")
    @patch("azureml.automl.dnn.nlp.ner.runner.prepare_post_run_properties")
    @patch("azureml.automl.dnn.nlp.ner.runner.Run")
    @patch("azureml.automl.dnn.nlp.ner.io.read.dataloader.NLPNERDataValidator")
    def test_runner_mltable_data_json(
            self,
            validator_mock,
            run_mock,
            post_run_mock,
            conda_yml_mock,
            save_model_mock,
            initialize_log_server_mock,
            unique_dir_mock,
            dataset_load_mock,
            tokenizer_factory_mock,
            model_factory_mock,
            config_factory_mock,
            trainer_mock,
            path_resolver_mock
    ):
        # run mock
        mock_run = MockRun()
        run_mock.get_context.return_value = mock_run

        # settings mock
        automl_settings = {
            "task_type": "text-ner",
            "primary_metric": "accuracy"
        }
        mltable_data_json = '{"TrainData": {"Uri": "azuremluri", "ResolvedUri": "resolved_uri"}, ' \
                            '"ValidData": {"Uri": "azuremluri2", "ResolvedUri": "resolved_uri2"}}'
        mock_settings = MagicMock()
        mock_settings.primary_metric = "accuracy"
        mock_settings.save_mlflow = True
        initialize_log_server_mock.return_value = mock_settings
        unique_dir_mock.return_value = "ner_data"

        # Load and validate dataset mocks
        dataset_load_mock.return_value = file_dataset_mock()
        validator_mock.return_value = MockValidator()

        # Trainer mock
        mock_trainer = ner_trainer_mock()
        trainer_mock.return_value = mock_trainer

        # Test runner
        runner.run(automl_settings, mltable_data_json)

        # Asserts
        mock_trainer.train.assert_called_once()
        mock_trainer.save_model.assert_called_once()
        mock_trainer.save_state.assert_called_once()
        self.assertEqual(model_factory_mock.call_args[0][0], "some_path")

    @patch("azureml.automl.dnn.nlp.ner.runner.log_metrics")
    @patch("azureml.automl.dnn.nlp.ner.runner.is_main_process")
    @patch("azureml.automl.dnn.nlp.ner.runner.NERPytorchTrainer")
    @patch("azureml.core.Dataset.get_by_id")
    @patch("azureml.automl.dnn.nlp.ner.runner.create_unique_dir")
    @patch("azureml.automl.dnn.nlp.ner.runner.initialize_log_server")
    @patch("azureml.automl.dnn.nlp.ner.runner.save_model_wrapper")
    @patch("azureml.automl.dnn.nlp.ner.runner.save_conda_yml")
    @patch("azureml.automl.dnn.nlp.ner.runner.AutoTokenizer.from_pretrained")
    @patch("azureml.automl.dnn.nlp.ner.runner.prepare_post_run_properties")
    @patch("azureml.automl.dnn.nlp.ner.runner.Run")
    @patch("azureml.automl.dnn.nlp.ner.io.read.dataloader.NLPNERDataValidator")
    @patch("azureml.automl.dnn.nlp.ner.runner.ModelWrapper")
    def test_runner_ort_scenario(
            self,
            model_wrapper_mock,
            validator_mock,
            run_mock,
            post_run_mock,
            tokenizer_factory_mock,
            conda_yml_mock,
            save_model_mock,
            initialize_log_server_mock,
            unique_dir_mock,
            get_by_id_mock,
            trainer_mock,
            is_main_process_mock,
            mock_metrics_logging,
            path_resolver_mock
    ):
        # Run and settings
        mock_run = MockRun()
        run_mock.get_context.return_value = mock_run

        automl_settings = {
            "task_type": "text-ner",
            "primary_metric": "accuracy",
            "dataset_id": "mock_dataset_id",
            "enable_distributed_dnn_training_ort_ds": True,
            "validation_dataset_id": "mock_validation_dataset_id"
        }
        mock_settings = MagicMock()
        mock_settings.dataset_id = "mock_dataset_id"
        mock_settings.validation_dataset_id = "mock_validation_dataset_id"
        mock_settings.primary_metric = "accuracy"
        mock_settings.enable_distributed_dnn_training_ort_ds = True
        mock_settings.save_mlflow = True
        initialize_log_server_mock.return_value = mock_settings
        unique_dir_mock.return_value = "ner_data"

        # Load and validate dataset mocks
        get_by_id_mock.return_value = file_dataset_mock()
        validator_mock.return_value = MockValidator()

        is_main_process_mock.return_value = True

        # Main process / ORT enabled
        runner.run(automl_settings)
        trainer_mock.assert_called_once()
        assert trainer_mock.call_args[1]["enable_distributed_ort_ds"] is True
        trainer_mock.return_value.train.assert_called_once()
        trainer_mock.return_value.validate.assert_called_once()
        mock_metrics_logging.assert_called_once()
        conda_yml_mock.assert_called_once()
        model_wrapper_mock.assert_called_once()
        assert trainer_mock.return_value.model == model_wrapper_mock.call_args[0][0]

        is_main_process_mock.return_value = False
        get_by_id_mock.return_value = file_dataset_mock()

        # ORT enabled / not main process
        runner.run(automl_settings)
        assert trainer_mock.call_count == 2
        assert trainer_mock.call_args[1]["enable_distributed_ort_ds"] is True
        assert trainer_mock.return_value.train.call_count == 2
        assert trainer_mock.return_value.validate.call_count == 2
        mock_metrics_logging.assert_called_once()

    @patch("azureml.automl.dnn.nlp.ner.runner.run_lifecycle_utilities.fail_run")
    @patch("azureml.automl.dnn.nlp.ner.runner.Run.get_context")
    def test_runner_exception_scrubbing(self, run_mock, mock_fail_run, path_resolver_mock):
        mock_run = MockRun()
        run_mock.return_value = mock_run

        automl_settings = {
            "task_type": "text-ner",
            "primary_metric": "accuracy"
        }

        with self.assertRaises(Exception):
            with patch("azureml.automl.dnn.nlp.ner.runner.is_data_labeling_run",
                       side_effect=Exception("It's a trap!")):
                runner.run(automl_settings)
        logged_exception = mock_fail_run.call_args[0][1]
        self.assertTrue(isinstance(logged_exception, ClientException))
        self.assertEqual(AutoNLPInternal.__name__, logged_exception.error_code)


if __name__ == "__main__":
    unittest.main()
