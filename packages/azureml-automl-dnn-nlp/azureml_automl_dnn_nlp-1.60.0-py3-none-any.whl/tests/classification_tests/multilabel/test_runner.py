from unittest.mock import patch, MagicMock, Mock

import importlib
import numpy as np
import unittest

from azureml.automl.core.shared.exceptions import ClientException, ValidationException
from azureml.automl.dnn.nlp.classification.multilabel import runner
from azureml.automl.dnn.nlp.common._diagnostics.nlp_error_definitions import AutoNLPInternal
from azureml.automl.dnn.nlp.common.constants import ModelNames
from ...mocks import MockRun, multilabel_trainer_mock

horovod_spec = importlib.util.find_spec("horovod")
has_horovod = horovod_spec is not None


class MockTrainingSet:
    def __init__(self):
        self.tokenizer = "some_tokenizer"
        self.data = "data"


class MockAutoMLSettings:
    def __init__(self, distributed, label_column_name):
        self.is_gpu = True
        self.dataset_id = "some_dataset_id"
        self.validation_dataset_id = "some_validation_dataset_id"
        self.label_column_name = label_column_name
        self.enable_distributed_dnn_training = distributed
        self.primary_metric = 'accuracy'
        self.featurization = "some_featurization"
        self.save_mlflow = True
        self.enable_code_generation = True


@patch("azureml.automl.dnn.nlp.common.training_configuration.ResourcePathResolver",
       return_value=Mock(model_name=ModelNames.BERT_BASE_UNCASED, model_path="some_path", tokenizer_path="some_path"))
@patch("azureml.automl.dnn.nlp.classification.multilabel.runner.AutoTokenizer.from_pretrained")
class MultilabelRunnerTests(unittest.TestCase):

    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.compute_metrics")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.ModelWrapper", return_value=None)
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.PytorchTrainer")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.load_and_validate_multilabel_dataset")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.initialize_log_server",
           return_value=MockAutoMLSettings(False, "labels"))
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_deploy_script", return_value="deploy_script")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner._get_input_example_dictionary",
           return_value="input_example")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner._get_output_example",
           return_value="output_example")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_conda_yml", return_value="conda_path")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_model_wrapper", return_value="model_path")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.Run.get_context")
    def test_runner(
            self,
            run_mock,
            save_model_mock,
            save_conda_mock,
            output_example_mock,
            input_example_mock,
            deploy_model_mock,
            initialize_log_server_mock,
            load_and_validate_multilabel_dataset_mock,
            trainer_mock,
            model_wrapper_mock,
            compute_metrics,
            tokenizer_factory_mock,
            path_resolver_mock
    ):
        automl_settings = {"is_gpu": True,
                           "dataset_id": "some_training_set",
                           "validation_dataset_id": "some_validation_set",
                           "label_column_name": "labels",
                           "enable_distributed_dnn_training": False}

        mock_run = MockRun(label_column_name="labels")
        run_mock.return_value = mock_run

        mocked_training_set = MockTrainingSet()
        train_label_list = np.array(["['label', 'A']", "['LabelA', '1', '2']", '[]'])
        dataset_loader_return = (mocked_training_set, "some_validation_set",
                                 5, train_label_list, "some_label_list",
                                 "some_y_val", "some_y_transformer")
        load_and_validate_multilabel_dataset_mock.return_value = dataset_loader_return

        metrics_dict = {
            "accuracy": 0.5,
            "f1_score_micro": 0.6,
            "f1_score_macro": 0.7
        }
        metrics_dict_with_thresholds = {
            "accuracy": [0.5],
            "precision": [0.6],
            "recall": [0.7]
        }
        compute_metrics.return_value = metrics_dict, metrics_dict_with_thresholds

        mocked_trainer = multilabel_trainer_mock(5)
        trainer_mock.return_value = mocked_trainer

        # Call Run
        runner.run(automl_settings)

        self.assertEquals(len(mock_run.properties), 10)
        self.assertEquals(mock_run.properties['primary_metric'], 'accuracy')
        self.assertEquals(mock_run.properties['score'], 0.5)
        self.assertEquals(mock_run.properties['run_algorithm'], ModelNames.BERT_BASE_UNCASED)

        mocked_trainer.train.assert_called_once()
        self.assertEqual(mocked_trainer.train.call_args[0][0], mocked_training_set)
        self.assertEqual(mocked_trainer.train.call_args[0][1], "some_validation_set")

        self.assertEqual(mock_run.metrics["accuracy"], 0.5)
        self.assertEqual(mock_run.metrics["f1_score_micro"], 0.6)
        self.assertEqual(mock_run.metrics["f1_score_macro"], 0.7)

    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.initialize_log_server",
           return_value=MockAutoMLSettings(False, None))
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.Run.get_context")
    def test_runner_without_label_col(
            self,
            run_mock,
            initialize_log_server_mock,
            tokenizer_factory_mock,
            path_resolver_mock
    ):
        automl_settings = {"is_gpu": True,
                           "dataset_id": "some_training_set",
                           "validation_dataset_id": "some_validation_set",
                           "label_column_name": None,
                           "enable_distributed_dnn_training": False}

        mock_run = MockRun()
        run_mock.return_value = mock_run

        # Call Run
        with self.assertRaises(ValidationException):
            runner.run(automl_settings)

        # Exception is raised and none of the trainer code gets executed
        self.assertEqual(len(mock_run.properties), 1)
        self.assertIn("errors", mock_run.properties)
        self.assertTrue(mock_run.metrics == {})

    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.compute_metrics")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.ModelWrapper", return_value=None)
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.PytorchTrainer")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.load_and_validate_multilabel_dataset")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.initialize_log_server",
           return_value=MockAutoMLSettings(False, "labels"))
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_deploy_script", return_value="deploy_script")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner._get_input_example_dictionary",
           return_value="input_example")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner._get_output_example",
           return_value="output_example")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_conda_yml", return_value="conda_path")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_model_wrapper", return_value="model_path")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.Run.get_context")
    def test_runner_labeling_service(
            self,
            run_mock,
            save_model_mock,
            save_conda_mock,
            output_example_mock,
            input_example_mock,
            deploy_model_mock,
            initialize_log_server_mock,
            load_and_validate_multilabel_dataset_mock,
            trainer_mock,
            model_wrapper_mock,
            compute_metrics,
            tokenizer_factory_mock,
            path_resolver_mock
    ):
        automl_settings = {"is_gpu": True,
                           "dataset_id": "some_training_set",
                           "validation_dataset_id": "some_validation_set",
                           "label_column_name": "labels",
                           "enable_distributed_dnn_training": False}

        mock_run = MockRun(run_source="Labeling", label_column_name="labels", labeling_dataset_type="FileDataset")
        run_mock.return_value = mock_run

        mocked_training_set = MockTrainingSet()
        dataset_loader_return = (mocked_training_set, "some_validation_set", 3,
                                 np.array(["['label', 'A']", "['LabelA', '1', '2']", '[]']), "some_label_list",
                                 "some_y_val", "some_y_transformer")
        load_and_validate_multilabel_dataset_mock.return_value = dataset_loader_return

        mocked_trainer = multilabel_trainer_mock(5)
        trainer_mock.return_value = mocked_trainer

        metrics_dict = {
            "accuracy": 0.5,
            "f1_score_micro": 0.6,
            "f1_score_macro": 0.7
        }
        metrics_dict_with_thresholds = {
            "accuracy": [0.5],
            "precision": [0.6],
            "recall": [0.7]
        }
        compute_metrics.return_value = metrics_dict, metrics_dict_with_thresholds

        # Call Run
        runner.run(automl_settings)

        self.assertEqual(len(mock_run.properties), 10)
        self.assertEqual(mock_run.properties['primary_metric'], 'accuracy')
        self.assertEqual(mock_run.properties['score'], 0.5)

        self.assertEquals(trainer_mock.call_args[1]["training_configuration"]["model_name"],
                          ModelNames.BERT_BASE_UNCASED)
        mocked_trainer.train.assert_called_once()
        self.assertEquals(mocked_trainer.train.call_args[0][0], mocked_training_set)
        self.assertEquals(mocked_trainer.train.call_args[0][1], "some_validation_set")

        self.assertEqual(mock_run.metrics["accuracy"], 0.5)
        self.assertEqual(mock_run.metrics["f1_score_micro"], 0.6)
        self.assertEqual(mock_run.metrics["f1_score_macro"], 0.7)

    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.initialize_log_server",
           return_value=MockAutoMLSettings(False, None))
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.Run.get_context")
    def test_runner_without_validation_data(
            self,
            run_mock,
            initialize_log_server_mock,
            tokenizer_factory_mock,
            path_resolver_mock
    ):
        automl_settings = {"is_gpu": True,
                           "dataset_id": "some_training_set",
                           "validation_dataset_id": None,
                           "label_column_name": "labels",
                           "enable_distributed_dnn_training": False}

        mock_run = MockRun()
        run_mock.return_value = mock_run

        # Call Run
        with self.assertRaises(ValidationException):
            runner.run(automl_settings)

        # Exception is raised and none of the trainer code gets executed
        self.assertEqual(len(mock_run.properties), 1)
        self.assertIn("errors", mock_run.properties)
        self.assertTrue(mock_run.metrics == {})

    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.compute_metrics")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.ModelWrapper", return_value=None)
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.PytorchTrainer")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.load_and_validate_multilabel_dataset")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.initialize_log_server",
           return_value=MockAutoMLSettings(False, "labels"))
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_deploy_script", return_value="deploy_script")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner._get_input_example_dictionary",
           return_value="input_example")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner._get_output_example",
           return_value="output_example")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_conda_yml", return_value="conda_path")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_model_wrapper", return_value="model_path")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.Run.get_context")
    def test_runner_mltable_data_json(
            self,
            run_mock,
            save_model_mock,
            save_conda_mock,
            output_example_mock,
            input_example_mock,
            deploy_model_mock,
            initialize_log_server_mock,
            load_and_validate_multilabel_dataset_mock,
            trainer_mock,
            model_wrapper_mock,
            compute_metrics,
            tokenizer_factory_mock,
            path_resolver_mock
    ):
        automl_settings = {"is_gpu": True,
                           "label_column_name": "labels",
                           "enable_distributed_dnn_training": False}

        mltable_data_json = '{"TrainData": {"Uri": "azuremluri", "ResolvedUri": "resolved_uri"}, ' \
                            '"ValidData": {"Uri": "azuremluri2", "ResolvedUri": "resolved_uri2"}}'

        mock_run = MockRun(run_source="Labeling", label_column_name="labels", labeling_dataset_type="FileDataset")
        run_mock.return_value = mock_run

        mocked_training_set = MockTrainingSet()
        dataset_loader_return = (mocked_training_set, "some_validation_set", 3,
                                 np.array(["['label', 'A']", "['LabelA', '1', '2']", '[]']), "some_label_list",
                                 "some_y_val", "some_y_transformer")
        load_and_validate_multilabel_dataset_mock.return_value = dataset_loader_return

        mocked_trainer = multilabel_trainer_mock(5)
        trainer_mock.return_value = mocked_trainer

        metrics_dict = {
            "accuracy": 0.5,
            "f1_score_micro": 0.6,
            "f1_score_macro": 0.7
        }
        metrics_dict_with_thresholds = {
            "accuracy": [0.5],
            "precision": [0.6],
            "recall": [0.7]
        }
        compute_metrics.return_value = metrics_dict, metrics_dict_with_thresholds

        # Call Run
        runner.run(automl_settings, mltable_data_json)

        self.assertTrue(load_and_validate_multilabel_dataset_mock.call_args[0][6] == mltable_data_json)

    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.run_lifecycle_utilities.fail_run")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.Run.get_context")
    def test_runner_exception_scrubbing(self, run_mock, mock_fail_run, tokenizer_factory_mock, path_resolver_mock):
        mock_run = MockRun()
        run_mock.return_value = mock_run

        automl_settings = {
            "task_type": "text-classification-multilabel",
            "primary_metric": "accuracy",
            "label_column_name": "labels_col"
        }

        with self.assertRaises(Exception):
            with patch("azureml.automl.dnn.nlp.classification.multilabel.runner."
                       "is_data_labeling_run_with_file_dataset", side_effect=Exception("It's a trap!")):
                runner.run(automl_settings)
        logged_exception = mock_fail_run.call_args[0][1]
        self.assertTrue(isinstance(logged_exception, ClientException))
        self.assertEquals(AutoNLPInternal.__name__, logged_exception.error_code)

    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.is_main_process")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner._metrics_logging")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.compute_metrics")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.ModelWrapper", return_value=None)
    @patch("azureml.automl.dnn.nlp.classification.multilabel.trainer.AutoModelForSequenceClassification")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.PytorchTrainer")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.load_and_validate_multilabel_dataset")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.initialize_log_server",
           return_value=MockAutoMLSettings(False, "labels"))
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_deploy_script", return_value="deploy_script")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner._get_input_example_dictionary",
           return_value="input_example")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner._get_output_example",
           return_value="output_example")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_conda_yml", return_value="conda_path")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.save_model_wrapper", return_value="model_path")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.initialize_log_server")
    @patch("azureml.automl.dnn.nlp.classification.multilabel.runner.Run.get_context")
    def test_runner_ort_scenario(
            self,
            run_mock, init_log_server_mock,
            save_model_mock,
            save_conda_mock,
            deploy_model_mock,
            input_example_mock,
            output_example_mock,
            initialize_log_server_mock,
            load_and_validate_multilabel_dataset_mock,
            trainer_mock,
            model_mock,
            model_wrapper_mock,
            mock_compute_metrics,
            mock_metrics_logging,
            is_main_process_mock,
            tokenizer_factory_mock,
            path_resolver_mock
    ):
        mock_run = MockRun(label_column_name="labels")
        run_mock.return_value = mock_run

        automl_settings = {"is_gpu": True,
                           "dataset_id": "some_training_set",
                           "validation_dataset_id": "some_validation_set",
                           "label_column_name": "labels",
                           "enable_distributed_dnn_training_ort_ds": True}

        mocked_training_set = MockTrainingSet()
        train_label_list = np.array(["['label', 'A']", "['LabelA', '1', '2']", '[]'])
        dataset_loader_return = (mocked_training_set, "some_validation_set",
                                 5, train_label_list, "some_label_list",
                                 "some_y_val", "some_y_transformer")
        load_and_validate_multilabel_dataset_mock.return_value = dataset_loader_return

        metrics_dict = {
            "accuracy": 0.5,
            "f1_score_micro": 0.6,
            "f1_score_macro": 0.7
        }
        metrics_dict_with_thresholds = {
            "accuracy": [0.5],
            "precision": [0.6],
            "recall": [0.7]
        }
        mock_compute_metrics.return_value = metrics_dict, metrics_dict_with_thresholds

        model = MagicMock()
        model.from_pretrained.return_value = MagicMock()
        model_mock.from_pretrained.return_value = model

        mocked_trainer = multilabel_trainer_mock(5)
        trainer_mock.return_value = mocked_trainer

        # set log values
        mock_settings = MagicMock()
        mock_settings.dataset_id = "mock_dataset_id"
        mock_settings.validation_dataset_id = "mock_validation_dataset_id"
        mock_settings.primary_metric = "accuracy"
        mock_settings.enable_distributed_dnn_training_ort_ds = True
        initialize_log_server_mock.return_value = mock_settings

        is_main_process_mock.return_value = True

        # Call Run
        runner.run(automl_settings)
        trainer_mock.assert_called_once()
        assert trainer_mock.call_args[1]["enable_distributed_ort_ds"] is True
        trainer_mock.return_value.train.assert_called_once()
        trainer_mock.return_value.validate.assert_called_once()
        mock_compute_metrics.assert_called_once()
        mock_metrics_logging.log_metrics.assert_called_once()
        save_conda_mock.assert_called_once()
        model_wrapper_mock.assert_called_once()
        assert trainer_mock.return_value.model == model_wrapper_mock.call_args[0][0]

        is_main_process_mock.return_value = False

        # ORT enabled / not main process
        runner.run(automl_settings)
        assert trainer_mock.call_count == 2
        assert trainer_mock.call_args[1]["enable_distributed_ort_ds"] is True
        assert trainer_mock.return_value.train.call_count == 2
        assert trainer_mock.return_value.validate.call_count == 2
        mock_compute_metrics.assert_called_once()
        mock_metrics_logging.log_metrics.assert_called_once()
        save_conda_mock.assert_called_once()
