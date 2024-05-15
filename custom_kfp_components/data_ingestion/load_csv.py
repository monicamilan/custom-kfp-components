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
from kfp.dsl import Dataset, Output
from typing import List, Callable

from custom_kfp_components.components import ComponentsBuilder, Components


class LoadCsvBuilder(ComponentsBuilder):
    """
    Class intended to load csv files into a pandas dataframe.
    """
    @staticmethod
    def _load_csv(file_path: str, dataset: Output[Dataset]) -> None:
        """
        Private method containing the code needed to load a csv into a pandas dataframe.

        :param file_path: Local or remote csv path
        :param dataset: Output artifact
        :return: None
        """
        import pandas as pd  # Import libraries

        df = pd.read_csv(file_path)
        df.to_csv(dataset.path, index=False)  # Store Dataframe

    @staticmethod
    def get_requirements() -> List[str]:
        return ['pandas==2.2.2']

    def component_function(self) -> Callable:
        return self._load_csv


class LoadCsv(Components):
    IMPLEMENTATION_CLASS = LoadCsvBuilder
