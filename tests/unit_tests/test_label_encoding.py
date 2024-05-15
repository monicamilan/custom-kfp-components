"""
Copyright 2024 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from typing import Callable

import pandas as pd
import pytest

from unittest import mock
from unittest.mock import MagicMock

from custom_kfp_components.data_preparation.label_encoding import LabelEncodingBuilder


@pytest.fixture
def mock_df() -> pd.DataFrame:
    return pd.DataFrame({'col_a': [1, 2, 3],
                         'col_b': [4, 5, 6],
                         'test_label': ['blue', 'blue', 'red']})


@pytest.fixture
def encoded_df() -> pd.DataFrame:
    return pd.DataFrame({'col_a': [1, 2, 3],
                         'col_b': [4, 5, 6],
                         'test_label': [0, 0, 1]})


def test_label_encoding(mock_df, encoded_df) -> None:
    with mock.patch("pandas.read_csv") as read_csv_mock:
        input_dataset = MagicMock()
        encoded_dataset = MagicMock()

        read_csv_mock.return_value = mock_df

        encoder = LabelEncodingBuilder(base_image='test')
        encoder._label_encoding(label_name='test_label',
                                input_dataset=input_dataset,
                                encoded_dataset=encoded_dataset)

        assert mock_df.equals(encoded_df)


def test_load_csv_args():
    with pytest.raises(TypeError):
        data_load = LabelEncodingBuilder(base_image='test')
        data_load._label_encoding(wrong_arg='test')


def test_get_requirements():
    encoder = LabelEncodingBuilder(base_image='test')
    assert encoder.get_requirements() == ['pandas', 'scikit-learn']


def test_component_function():
    encoder = LabelEncodingBuilder(base_image='test')
    assert isinstance(encoder.component_function(), Callable)
