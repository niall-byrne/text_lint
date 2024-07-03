"""Test the ValidatorBase class."""

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from ..validator_base import ValidatorBase


class TestValidatorBase:
  """Test the ValidatorBase class."""

  def test_initialize__defined__attributes(
      self,
      concrete_validator_base_instance: ValidatorBase,
      mocked_validator_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "mocked_validator_base_hint",
        "name": mocked_validator_name,
        "operation": "mocked_validator_base_operation",
        "yaml_example": "mocked_validator_base_yaml_example",
    }

    assert_operation_attributes(
        concrete_validator_base_instance,
        attributes,
    )

  def test_initialize__inheritance(
      self,
      concrete_validator_base_instance: ValidatorBase,
  ) -> None:
    assert_operation_inheritance(
        concrete_validator_base_instance,
        bases=(ValidatorBase,),
    )
