"""Test the ValidationBase class."""

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from ..validator_base import ValidationBase


class TestValidationBase:
  """Test the ValidationBase class."""

  def test_initialize__defined__attributes(
      self,
      concrete_validator_base_instance: ValidationBase,
      mocked_validator_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "mocked_hint",
        "name": mocked_validator_name,
        "operation": "mocked_operation",
    }

    assert_operation_attributes(
        concrete_validator_base_instance,
        attributes,
    )

  def test_initialize__inheritance(
      self,
      concrete_validator_base_instance: ValidationBase,
  ) -> None:
    assert_operation_inheritance(
        concrete_validator_base_instance,
        bases=(ValidationBase,),
    )
