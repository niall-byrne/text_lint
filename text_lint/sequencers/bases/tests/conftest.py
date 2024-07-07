"""Test fixtures for the text file linter."""

from typing import List, Type
from unittest import mock

import pytest
from ..operator_base import OperatorBase


@pytest.fixture
def mocked_operations() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock(), mock.Mock()]


@pytest.fixture
def concrete_operator_class() -> Type[OperatorBase[mock.Mock]]:

  class ConcreteSequencer(OperatorBase[mock.Mock]):
    pass

  return ConcreteSequencer
