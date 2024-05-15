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
from kfp.dsl import Dataset, Output, Input
from typing import Callable, List

from custom_kfp_components.components import Components, ComponentsBuilder


class LabelEncodingBuilder(ComponentsBuilder):
    """
    Class intended to apply label encoding to a column of a pandas dataframe.
    """
    @staticmethod
    def _label_encoding(label_name: str, input_dataset: Input[Dataset], encoded_dataset: Output[Dataset]) -> None:
        """
        Private method containing the code needed to apply label encoding.

        :param label_name: Column name to encode
        :param input_dataset: Input artifact
        :param encoded_dataset: Output artifact
        :return: None
        """
        import pandas as pd  # Import libraries
        from sklearn.preprocessing import LabelEncoder

        df = pd.read_csv(input_dataset.path)

        encoder = LabelEncoder()
        df[label_name] = encoder.fit_transform(df[label_name])
        df.to_csv(encoded_dataset.path, index=False)  # Store Dataframe

    @staticmethod
    def get_requirements() -> List[str]:
        return ['pandas', 'scikit-learn']

    def component_function(self) -> Callable:
        return self._label_encoding


class LabelEncoding(Components):
    IMPLEMENTATION_CLASS = LabelEncodingBuilder
