# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Utility functions for multi-class classification."""

import logging
import numpy as np
import os
import pandas as pd
import scipy
from transformers import AutoTokenizer
from typing import Any, Dict, Union

from azureml.automl.core.shared import constants
from azureml.automl.dnn.nlp.classification.common.constants import MultiClassInferenceLiterals
from azureml.automl.dnn.nlp.common._utils import concat_text_columns
from azureml.automl.dnn.nlp.common.constants import OutputLiterals, TrainingInputLiterals
from azureml.automl.dnn.nlp.common.training_configuration import TrainingConfiguration
from azureml.automl.runtime._ml_engine import evaluate_classifier

_logger = logging.getLogger(__name__)


def compute_metrics(y_val: np.ndarray, predictions: np.ndarray, class_labels: np.ndarray,
                    train_labels: np.ndarray) -> Dict[str, Union[float, Dict[str, Any]]]:
    """
    Function to compute metrics like accuracy and auc-weighted

    :param predictions: Predictions on the validation/test dataset used for computing metrics.
    :return: A dictionary mapping metric name to metric score.
    """
    probas = scipy.special.softmax(predictions, axis=1)
    metrics_names = list(constants.Metric.CLASSIFICATION_SET)
    return evaluate_classifier(y_val, probas, metrics_names, class_labels, train_labels)


def get_max_seq_length(train_df: pd.DataFrame,
                       tokenizer: AutoTokenizer,
                       label_column_name: str,
                       training_configuration: TrainingConfiguration,
                       enable_long_range_text: bool = True) -> int:
    """
    Default value for max_seq_length is 128.

    If the user opts in for long range text, we use this heuristic to determine optimal max_seq_length value.

    If the fraction of training examples with length of the text document exceeding 128 tokens/words
    is greater than an empirically determined threshold, then use a higher value for max_seq_length.
    Currently it gets set to 256 rather than 128 if the aforementioned condition is satisfied.

    :param train_df: training data to be leveraged for computing max_seq_length
    :param tokenizer: tokenizer to be used to tokenize the data
    :param label_column_name: Name/title of the label column
    :param training_configuration: a collection of parameters to dictate the training procedure.
    :param enable_long_range_text: param to enable long range text calculation. True by default.
    :return: dynamically computed max sequence length
    """
    max_seq_length = training_configuration[TrainingInputLiterals.MAX_SEQ_LENGTH]
    if enable_long_range_text:
        text_len = []
        for _, row in train_df.iterrows():
            concatenated_text_from_train_sample = concat_text_columns(row, train_df.columns, label_column_name)
            tokenized = tokenizer.tokenize(concatenated_text_from_train_sample)
            text_len.append(len(tokenized))

        default_range_frac = sum(i > training_configuration[TrainingInputLiterals.MAX_SEQ_LENGTH]
                                 for i in text_len) / len(text_len)
        long_range_frac = sum(i > training_configuration[TrainingInputLiterals.LONG_RANGE_LENGTH]
                              for i in text_len) / len(text_len)
        _logger.info(f"Dataset Stats: Mean length of text={np.mean(text_len)}\n"
                     f"Max length of text={np.max(text_len)}\n"
                     f"Median length of text={np.median(text_len)}\n"
                     f"Fraction of number of rows with len of text longer than "
                     f"{training_configuration[TrainingInputLiterals.MAX_SEQ_LENGTH]} tokens={default_range_frac}\n"
                     f"Fraction of number of rows with len of text longer than "
                     f"{training_configuration[TrainingInputLiterals.LONG_RANGE_LENGTH]} tokens={long_range_frac}")

        if default_range_frac >= training_configuration[TrainingInputLiterals.LONG_RANGE_THRESHOLD]:
            max_seq_length = training_configuration[TrainingInputLiterals.LONG_RANGE_LENGTH]
    _logger.info("Based on dataset characteristics, Max Sequence Length = {}".format(max_seq_length))

    if not os.path.exists(OutputLiterals.OUTPUT_DIR):
        os.mkdir(OutputLiterals.OUTPUT_DIR)
    np.save(OutputLiterals.OUTPUT_DIR + '/' + MultiClassInferenceLiterals.MAX_SEQ_LENGTH, max_seq_length)

    return max_seq_length
