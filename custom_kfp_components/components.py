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
import abc
from abc import ABC

from kfp import dsl
from kfp.dsl.python_component import PythonComponent

from typing import List, Callable

BASE_IMAGE = 'python:3.9'


class ComponentsBuilder(ABC):
    """
    Parent class intended to create the logic needed to build Kubeflow components.
    """
    def __init__(self, base_image: str):
        self.base_image = base_image

    @abc.abstractmethod
    def component_function(self) -> Callable:
        """
        Public method that needs to be overridden to encapsulate a function.

        :return: Function to be executed in the container
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def get_requirements() -> List[str]:
        """
        Public method that needs to be overridden to return the list of required packages to be installed.

        :return: List of requirements
        """
        return []

    def build(self, **kwargs) -> PythonComponent:
        """
        Public method that returns a Kubeflow component object.

        :param kwargs:
        :return: Kubeflow component
        """
        return dsl.component(func=self.component_function(),
                             base_image=self.base_image,
                             packages_to_install=self.get_requirements())(**kwargs)


class Components:

    IMPLEMENTATION_CLASS = ComponentsBuilder

    def __new__(cls, base_image=BASE_IMAGE, **kwargs):
        return cls.IMPLEMENTATION_CLASS(base_image).build(**kwargs)
