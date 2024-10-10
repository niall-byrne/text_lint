"""Test the OperationBase class."""

from typing import Any

from text_lint.operations.bases.operation_base import OperationBase
from text_lint.operations.mixins.parameter_validation import (
    ParameterValidationMixin,
)


class TestOperationBase:
  """Test the OperationBase class."""

  def test_intialize__defaults__attributes(
      self,
      concrete_operation_base_instance: OperationBase[Any],
  ) -> None:
    assert concrete_operation_base_instance.internal_use_only is False

  def test_initialize__inheritance(
      self,
      concrete_operation_base_instance: OperationBase[Any],
  ) -> None:
    assert isinstance(
        concrete_operation_base_instance,
        ParameterValidationMixin,
    )
    assert isinstance(
        concrete_operation_base_instance,
        OperationBase,
    )
