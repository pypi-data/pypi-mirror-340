from unittest.mock import MagicMock, patch
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import unittest

from azureml.automl.core.shared.exceptions import DataException
from azureml.automl.dnn.nlp.classification.common.constants import DatasetLiterals
from azureml.automl.dnn.nlp.classification.io.read._labeling_data_helper import _convert_to_dict_entry
from azureml.automl.dnn.nlp.classification.io.read.dataloader import load_and_validate_multiclass_dataset
from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import MulticlassDatasetWrapper
from azureml.automl.dnn.nlp.common._diagnostics.nlp_error_definitions import (
    InsufficientUniqueLabels, IncorrectClassificationDatasetType, MissingDataset
)
from azureml.automl.dnn.nlp.common._utils import concat_text_columns
from azureml.automl.dnn.nlp.common.constants import \
    DataLiterals, Split, TrainingInputLiterals, TrainingDefaultSettings
from azureml.automl.dnn.nlp.common.training_configuration import TrainingConfiguration

from ...mocks import (
    aml_dataset_mock, aml_label_dataset_mock, file_dataset_mock, get_multiclass_labeling_df, open_classification_file
)
try:
    import torch
    has_torch = True
except ImportError:
    has_torch = False


@pytest.mark.usefixtures('MulticlassDatasetTester')
@pytest.mark.usefixtures('MulticlassTokenizer')
class TestTextClassificationDataLoadTests:
    @pytest.fixture(autouse=True)
    def _before_each(self):
        self.training_configuration = TrainingConfiguration(
            {TrainingInputLiterals.MAX_SEQ_LENGTH: TrainingDefaultSettings.DEFAULT_SEQ_LEN,
             TrainingInputLiterals.PADDING_STRATEGY: TrainingDefaultSettings.MAX_LENGTH,
             TrainingInputLiterals.LONG_RANGE_LENGTH: TrainingDefaultSettings.LONG_RANGE_MAX,
             TrainingInputLiterals.LONG_RANGE_THRESHOLD: TrainingDefaultSettings.MIN_PROPORTION_LONG_RANGE},
            _internal=True)
        yield

    """Tests for Text Classification data loader."""
    @pytest.mark.parametrize('multiple_text_column', [True, False])
    @pytest.mark.parametrize('include_label_col', [True, False])
    def test_concat_text_and_preserve_label(self, MulticlassDatasetTester, include_label_col, MulticlassTokenizer):
        input_df = MulticlassDatasetTester.get_data().copy()
        multiple_cols = MulticlassDatasetTester.multiple_text_column
        label_column_name = "labels_col"

        if include_label_col:
            label_list = pd.unique(input_df[label_column_name])
            dataset = MulticlassDatasetWrapper(input_df, label_list, MulticlassTokenizer,
                                               self.training_configuration, label_column_name)
            assert len(dataset[0]) == 4
        else:
            label_list = np.array(["train_label_1", "train_label_2"])
            dataset = MulticlassDatasetWrapper(input_df, label_list, MulticlassTokenizer,
                                               self.training_configuration)
            len(dataset[0]) == 3

        input_ids = [item for item in dataset[0][DatasetLiterals.INPUT_IDS] if item != 0]
        if multiple_cols:
            # col 2, row 1 has 5 tokens (see conftest), and col 1, row 1 has 10
            len(input_ids) == 15
        else:
            # col 1, row 1 has 10 tokens (see conftest)
            len(input_ids) == 10

    @unittest.skipIf(not has_torch, "torch not installed")
    @pytest.mark.parametrize('multiple_text_column', [True, False])
    @pytest.mark.parametrize('include_label_col', [True])
    def test_pytorch_multiclass_dataset_wrapper(self, MulticlassDatasetTester,
                                                multiple_text_column, MulticlassTokenizer):
        input_df = MulticlassDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        label_list = pd.unique(input_df[label_column_name])

        # Will handle None Type values
        row_num = 4
        input_df['text_first'][row_num] = None
        output_set = MulticlassDatasetWrapper(input_df, label_list, MulticlassTokenizer,
                                              self.training_configuration, label_column_name)
        # To check the addition of a period between the concatenated strings.
        # input_df's text columns on the 4th row don't have any period before concatenation.
        if multiple_text_column:
            assert "." in concat_text_columns(input_df.iloc[row_num], input_df.columns, label_column_name)

        assert output_set.max_seq_length == self.training_configuration[TrainingInputLiterals.MAX_SEQ_LENGTH]
        assert type(output_set) == MulticlassDatasetWrapper
        assert len(output_set) == 50
        for i in range(len(output_set)):
            training_keys = {DataLiterals.LABEL_COLUMN, DatasetLiterals.INPUT_IDS,
                             DatasetLiterals.TOKEN_TYPE_IDS, DatasetLiterals.ATTENTION_MASK}
            assert all([item in training_keys for item in output_set[i].keys()])
            assert all([type(item) == torch.Tensor for item in output_set[i].values()])

    @pytest.mark.parametrize('multiple_text_column', [True, False])
    @pytest.mark.parametrize('include_label_col', [True])
    @pytest.mark.parametrize(
        'mltable_data_json', [
            None,
            '{"TrainData": {"Uri": "azuremluri", "ResolvedUri": "resolved_uri"}, '
            '"ValidData": {"Uri": "azuremluri2", "ResolvedUri": "resolved_uri2"}}'
        ]
    )
    @pytest.mark.parametrize('is_long_range_text', [True, False])
    @pytest.mark.parametrize('enable_long_range_text', [True, False])
    @patch("azureml.data.abstract_dataset.AbstractDataset._load")
    @patch("azureml.core.Dataset.get_by_id")
    def test_load_and_validate_multiclass_dataset(self, get_by_id_mock, dataset_load_mock, MulticlassDatasetTester,
                                                  is_long_range_text, mltable_data_json, MulticlassTokenizer,
                                                  enable_long_range_text):
        input_df = MulticlassDatasetTester.get_data(is_long_range_text).copy()
        label_column_name = "labels_col"
        mock_aml_dataset = aml_dataset_mock(input_df.copy())
        get_by_id_mock.return_value = mock_aml_dataset
        dataset_load_mock.return_value = mock_aml_dataset
        automl_settings = dict()
        automl_settings['dataset_id'] = 'mock_id'
        automl_settings['validation_dataset_id'] = 'mock_validation_id'
        aml_workspace_mock = MagicMock()
        training_set, validation_set, label_list, _, y_val = load_and_validate_multiclass_dataset(
            aml_workspace_mock, DataLiterals.DATA_DIR, label_column_name,
            MulticlassTokenizer, automl_settings, self.training_configuration, mltable_data_json=mltable_data_json,
            enable_long_range_text=enable_long_range_text
        )
        assert all(np.array(input_df[label_column_name]) == y_val)
        # The returned label_list is sorted, although the original labels weren't
        input_label_list = input_df[label_column_name].unique()
        assert any(label_list != input_label_list)
        input_label_list.sort()
        assert all(label_list == input_label_list)
        for output_set in [training_set, validation_set]:
            assert type(output_set) == MulticlassDatasetWrapper
            assert len(output_set) == 50
            if enable_long_range_text and is_long_range_text:
                assert output_set.max_seq_length == TrainingDefaultSettings.LONG_RANGE_MAX
                assert self.training_configuration[TrainingInputLiterals.MAX_SEQ_LENGTH] \
                       == TrainingDefaultSettings.LONG_RANGE_MAX
            else:
                assert output_set.max_seq_length == TrainingDefaultSettings.DEFAULT_SEQ_LEN
        for i in range(len(training_set)):
            training_keys = {DataLiterals.LABEL_COLUMN, DatasetLiterals.INPUT_IDS,
                             DatasetLiterals.TOKEN_TYPE_IDS, DatasetLiterals.ATTENTION_MASK}
            assert all([item in training_keys for item in training_set[i].keys()])
        for i in range(len(validation_set)):
            validation_keys = {DataLiterals.LABEL_COLUMN, DatasetLiterals.INPUT_IDS,
                               DatasetLiterals.TOKEN_TYPE_IDS, DatasetLiterals.ATTENTION_MASK}
            assert all([item in validation_keys for item in validation_set[i].keys()])

    @pytest.mark.parametrize('multiple_text_column', [False])
    @pytest.mark.parametrize('include_label_col', [True])
    @patch("azureml.core.Dataset.get_by_id")
    def test_one_unique_class_in_multiclass_dataset(self, get_by_id_mock, MulticlassDatasetTester,
                                                    MulticlassTokenizer):
        input_df = MulticlassDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        input_df[label_column_name] = "XYZ"
        mock_aml_dataset = aml_dataset_mock(input_df.copy())
        get_by_id_mock.return_value = mock_aml_dataset
        automl_settings = dict()
        automl_settings['dataset_id'] = 'mock_id'
        automl_settings['validation_dataset_id'] = 'mock_validation_id'
        aml_workspace_mock = MagicMock()

        with pytest.raises(DataException) as exc:
            load_and_validate_multiclass_dataset(
                workspace=aml_workspace_mock,
                data_dir=DataLiterals.DATA_DIR,
                label_column_name=label_column_name,
                tokenizer=MulticlassTokenizer,
                automl_settings=automl_settings,
                training_configuration=MagicMock()
            )
        assert exc.value.error_code == InsufficientUniqueLabels.__name__

    @pytest.mark.parametrize('multiple_text_column', [True, False])
    @pytest.mark.parametrize('include_label_col', [True])
    @pytest.mark.parametrize(
        'mltable_data_json', [
            None,
            '{"TrainData": {"Uri": "azuremluri", "ResolvedUri": "resolved_uri"}, '
            '"ValidData": null}'
        ]
    )
    @patch("azureml.data.abstract_dataset.AbstractDataset._load")
    @patch("azureml.core.Dataset.get_by_id")
    def test_load_and_validate_multiclass_dataset_no_val_df(self, get_by_id_mock, dataset_load_mock,
                                                            mltable_data_json, MulticlassDatasetTester,
                                                            MulticlassTokenizer):
        input_df = MulticlassDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        mock_aml_dataset = aml_dataset_mock(input_df.copy())
        get_by_id_mock.return_value = mock_aml_dataset
        dataset_load_mock.return_value = mock_aml_dataset
        automl_settings = dict()
        if mltable_data_json is None:
            automl_settings['dataset_id'] = 'mock_id'
        aml_workspace_mock = MagicMock()

        with pytest.raises(DataException) as exc:
            load_and_validate_multiclass_dataset(
                workspace=aml_workspace_mock,
                data_dir=DataLiterals.DATA_DIR,
                label_column_name=label_column_name,
                tokenizer=MulticlassTokenizer,
                automl_settings=automl_settings,
                training_configuration=MagicMock(),
                mltable_data_json=mltable_data_json
            )
        assert exc.value.error_code == MissingDataset.__name__
        assert Split.valid.value.capitalize() in exc.value.message_format

    @pytest.mark.parametrize('multiple_text_column', [False])
    @pytest.mark.parametrize('include_label_col', [True])
    @patch("azureml.core.Dataset.get_by_id")
    def test_load_and_validate_multiclass_dataset_non_tabular(self, get_by_id_mock,
                                                              MulticlassTokenizer):
        label_column_name = "labels_col"
        mock_aml_dataset = file_dataset_mock()
        get_by_id_mock.return_value = mock_aml_dataset
        automl_settings = dict()
        automl_settings['dataset_id'] = 'mock_id'
        automl_settings['validation_dataset_id'] = 'mock_validation_id'
        aml_workspace_mock = MagicMock()

        with pytest.raises(DataException) as exc:
            load_and_validate_multiclass_dataset(
                workspace=aml_workspace_mock,
                data_dir=DataLiterals.DATA_DIR,
                label_column_name=label_column_name,
                tokenizer=MulticlassTokenizer,
                automl_settings=automl_settings,
                training_configuration=MagicMock()
            )
        assert exc.value.error_code == IncorrectClassificationDatasetType.__name__


class TestUnparameterizedTextClassificationTests:
    @pytest.fixture(autouse=True)
    def _before_each(self):
        self.training_configuration = TrainingConfiguration(
            {TrainingInputLiterals.MAX_SEQ_LENGTH: TrainingDefaultSettings.DEFAULT_SEQ_LEN,
             TrainingInputLiterals.PADDING_STRATEGY: TrainingDefaultSettings.MAX_LENGTH,
             TrainingInputLiterals.LONG_RANGE_LENGTH: TrainingDefaultSettings.LONG_RANGE_MAX,
             TrainingInputLiterals.LONG_RANGE_THRESHOLD: TrainingDefaultSettings.MIN_PROPORTION_LONG_RANGE},
            _internal=True)
        yield

    @patch("azureml.core.Dataset.get_by_id")
    def test_load_and_validate_multiclass_dataset_labeling_service(self, get_by_id_mock, MulticlassTokenizer):
        label_column_name = "label"
        input_df = get_multiclass_labeling_df()
        mock_aml_dataset = aml_label_dataset_mock('TextClassificationMultiClass', input_df)
        get_by_id_mock.return_value = mock_aml_dataset
        automl_settings = dict()
        automl_settings['dataset_id'] = 'mock_id'
        automl_settings['validation_dataset_id'] = 'mock_validation_id'
        aml_workspace_mock = MagicMock()
        with patch("azureml.automl.dnn.nlp.classification.io.read._labeling_data_helper.open",
                   new=open_classification_file):
            training_set, validation_set, label_list, _, y_val = load_and_validate_multiclass_dataset(
                workspace=aml_workspace_mock,
                data_dir=DataLiterals.DATA_DIR,
                label_column_name=label_column_name,
                tokenizer=MulticlassTokenizer,
                automl_settings=automl_settings,
                training_configuration=self.training_configuration,
                is_labeling_run=True
            )
        assert training_set.max_seq_length == TrainingDefaultSettings.DEFAULT_SEQ_LEN
        assert all(np.array(input_df[label_column_name]) == y_val)
        input_label_list = input_df[label_column_name].unique()
        assert set(label_list) == set(input_label_list)
        for output_set in [training_set, validation_set]:
            assert type(output_set) == MulticlassDatasetWrapper
            assert len(output_set) == 60
        for i in range(len(training_set)):
            training_keys = {DataLiterals.LABEL_COLUMN, DatasetLiterals.INPUT_IDS,
                             DatasetLiterals.TOKEN_TYPE_IDS, DatasetLiterals.ATTENTION_MASK}
            assert all([item in training_keys for item in training_set[i].keys()])
        for i in range(len(validation_set)):
            validation_keys = {DataLiterals.LABEL_COLUMN, DatasetLiterals.INPUT_IDS,
                               DatasetLiterals.TOKEN_TYPE_IDS, DatasetLiterals.ATTENTION_MASK}
            assert all([item in validation_keys for item in validation_set[i].keys()])

    @patch("azureml.automl.dnn.nlp.classification.io.read.dataloader._load_dataframe")
    @patch("azureml.automl.dnn.nlp.classification.io.read.dataloader.get_max_seq_length")
    def test_load_and_validate_multiclass_dataset_handles_null_labels_correctly(self,
                                                                                get_max_seq_length,
                                                                                mock_dataset_loader):
        train_df = pd.DataFrame({"input_text_col": np.repeat(np.array(["Philodendron Pink Princess",
                                                                       "Philodendron Gloriosum",
                                                                       "Philodendron Dean McDowell",
                                                                       "Philodendron Pastazanum",
                                                                       "Philodendron Plowmanii"]), 20),
                                 "labels": np.repeat(np.array(["Good", "Great", "Best", None, None]), 20)})
        mock_dataset_loader.return_value = (train_df, None)
        get_max_seq_length.return_value = 128

        assert train_df.shape[0] == 100
        load_and_validate_multiclass_dataset(workspace=None,
                                             data_dir="",
                                             label_column_name="labels",
                                             tokenizer=MagicMock(model_max_length=128),
                                             automl_settings="",
                                             training_configuration=self.training_configuration)
        assert train_df.shape[0] == 60

    @patch("azureml.automl.dnn.nlp.classification.io.read.dataloader._load_dataframe")
    @patch("azureml.automl.dnn.nlp.classification.io.read.dataloader.get_max_seq_length")
    def test_load_and_validate_multiclass_dataset_handles_null_labels_int_correctly(self,
                                                                                    get_max_seq_length,
                                                                                    mock_dataset_loader):
        train_df = pd.DataFrame({"input_text_col": np.repeat(np.array(["Philodendron Pink Princess",
                                                                       "Philodendron Gloriosum",
                                                                       "Philodendron Dean McDowell",
                                                                       "Philodendron Pastazanum",
                                                                       "Philodendron Plowmanii"]), 20),
                                 "labels": np.repeat(np.array([1, 2, 3, None, None]), 20)})
        mock_dataset_loader.return_value = (train_df, None)
        get_max_seq_length.return_value = 128

        assert train_df.shape[0] == 100

        training_set, validation_set, label_list, label_list, y_val\
            = load_and_validate_multiclass_dataset(workspace=None,
                                                   data_dir="",
                                                   label_column_name="labels",
                                                   tokenizer=MagicMock(model_max_length=128),
                                                   automl_settings="",
                                                   training_configuration=self.training_configuration)
        assert train_df.shape[0] == 60
        assert training_set.data['labels'][2] == '1'
        assert training_set.data.shape[0] == 60

    @patch('azureml.automl.dnn.nlp.classification.io.read.dataloader.NLPMulticlassDataValidator')
    @patch('azureml.automl.dnn.nlp.classification.io.read.dataloader._load_dataframe')
    @patch('azureml.automl.dnn.nlp.classification.io.read.dataloader.get_max_seq_length')
    def test_load_and_validate_multiclass_with_unseen_validation_labels(self,
                                                                        get_max_seq_length,
                                                                        mock_dataset_loader,
                                                                        mock_validator):
        train_df = pd.DataFrame({"input_text_col": np.array(["Monstera Deliciosa",
                                                             "Calathea Majestica",
                                                             "Asparagus Fern"]),
                                 "health": np.array(["good", "bad", "good"])})
        valid_df = pd.DataFrame({"input_text_col": np.array(["Monstera Deliciosa",
                                                             "Calathea Majestica",
                                                             "Asparagus Fern"]),
                                 "health": np.array(["very good", "poor", "good"])})
        mock_dataset_loader.return_value = (train_df, valid_df)
        get_max_seq_length.return_value = 128
        _, _, train_label_list, label_list, _ = load_and_validate_multiclass_dataset(
            workspace=None,
            data_dir="",
            label_column_name="health",
            tokenizer=MagicMock(model_max_length=128),
            automl_settings="",
            training_configuration=self.training_configuration
        )

        expected_labels = {"good", "bad", "very good", "poor"}
        # For now, unseen valid labels are included in train set so model is aware of them for training.
        assert set(train_label_list) == expected_labels
        assert set(label_list) == expected_labels

    def test_wrapped_dataset_label_property(self):
        train_df = pd.DataFrame({"input_text_col": np.array(["Beep", "Boop", "Bop"]),
                                 "labels": np.array([1, 2, 3])})
        mock_tokenizer = MagicMock(model_max_length=128)
        wrapped_train = MulticlassDatasetWrapper(dataframe=train_df,
                                                 label_list=np.unique(train_df["labels"]),
                                                 tokenizer=mock_tokenizer,
                                                 training_configuration=self.training_configuration,
                                                 label_column_name="labels")
        assert (wrapped_train.labels == np.array([1, 2, 3])).all()

    def test_iter_wrapped_dataset_non_standard_indexed_dataframes(self):
        train_df = pd.DataFrame({"input_text_col": np.array(["Philodendron Spiritus Sancti",
                                                             "Philodendron Billietiae",
                                                             "Philodendron Ventricosum",
                                                             "Philodendron Domesticum",
                                                             "Philodendron Xanadu"]),
                                 "labels": np.array(["$$$", "$$", None, "$", "$"])})
        train_df.dropna(subset=["labels"], inplace=True)
        mock_tokenizer = MagicMock(model_max_length=128)
        mock_tokenizer.return_value = {DatasetLiterals.INPUT_IDS: np.array([]),
                                       DatasetLiterals.TOKEN_TYPE_IDS: np.array([]),
                                       DatasetLiterals.ATTENTION_MASK: np.array([])}
        wrapped_train = MulticlassDatasetWrapper(dataframe=train_df,
                                                 label_list=np.unique(train_df["labels"]),
                                                 tokenizer=mock_tokenizer,
                                                 training_configuration=self.training_configuration,
                                                 label_column_name="labels")
        assert wrapped_train[2][DataLiterals.LABEL_COLUMN] == wrapped_train.label_to_id["$"]

    def test_labeling_data_helper_convert_to_dict_entry_with_special_token(self):
        file_path = Path(__file__).parent.parent.parent / "data" / "data_with_special_tokens.txt"
        data_read = _convert_to_dict_entry(file_path, '', False)
        if DataLiterals.ERRORS == 'ignore':
            assert data_read[DataLiterals.TEXT_COLUMN] == "ABC"
        if DataLiterals.ERRORS == 'replace':
            assert data_read[DataLiterals.TEXT_COLUMN] == "\ufffdABC"
