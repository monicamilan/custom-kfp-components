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

from custom_kfp_components.data_ingestion.load_csv import LoadCsvBuilder


@pytest.fixture
def mock_df() -> pd.DataFrame:
    return pd.DataFrame({'col_a': [1, 2, 3], 'col_b': [4, 5, 6]})


def test_load_csv() -> None:
    with mock.patch("pandas.read_csv") as read_csv_mock:
        mock_df = MagicMock()
        mock_to_csv = MagicMock()
        dataset = MagicMock()

        mock_df.to_csv = mock_to_csv
        read_csv_mock.return_value = mock_df

        data_load = LoadCsvBuilder(base_image='test')
        data_load._load_csv(file_path='test.csv', dataset=dataset)

        mock_to_csv.assert_called_once_with(dataset.path, index=False)


def test_load_csv_args():
    with pytest.raises(TypeError):
        data_load = LoadCsvBuilder(base_image='test')
        data_load._load_csv(wrong_arg='test')


def test_get_requirements():
    assert LoadCsvBuilder.get_requirements() == ['pandas==2.2.2']


def test_component_function():
    encoder = LoadCsvBuilder(base_image='test')
    assert isinstance(encoder.component_function(), Callable)
