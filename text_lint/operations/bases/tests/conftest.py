"""Shared test fixtures for operation base classes."""
# pylint: disable=redefined-outer-name

from typing import Any, Type

import pytest
from text_lint.linter.states.bases.state_base import StateBase
from .. import operation_base


@pytest.fixture
def concrete_operation_base_class() -> Type[operation_base.OperationBase[Any]]:

  class ConcreteOperation(operation_base.OperationBase[Any]):

    def apply(self, state: "StateBase") -> None:
      """Concrete apply method implementation."""

  return ConcreteOperation


@pytest.fixture
def concrete_operation_base_instance(
    concrete_operation_base_class: Type[operation_base.OperationBase[Any]],
) -> operation_base.OperationBase[Any]:

  return concrete_operation_base_class()
