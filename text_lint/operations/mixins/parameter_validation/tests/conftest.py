"""Shared test fixtures for the operation mixin classes."""
# pylint: disable=redefined-outer-name

from typing import Any, Type

import pytest
from text_lint.operations.mixins import parameter_validation
# pylint: disable=wildcard-import,unused-wildcard-import
from .scenarios import *


class PersonClass:

  def __init__(self, name: Any, identifier: Any) -> None:
    self.name = name
    self.identifier = identifier


@pytest.fixture
def concrete_parameter_class(
) -> Type[parameter_validation.ParameterValidationMixin]:

  class ConcreteParameterClass(
      PersonClass,
      parameter_validation.ParameterValidationMixin,
  ):

    def __init__(self, name: Any, identifier: Any) -> None:
      super().__init__(name, identifier)
      self.validate_parameters()

  return ConcreteParameterClass
