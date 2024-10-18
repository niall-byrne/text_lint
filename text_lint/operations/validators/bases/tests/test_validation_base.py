"""Test the ValidatorBase class."""

from unittest import mock

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
    assert_parameter_schema,
    spy_on_validate_parameters,
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
        "internal_use_only": False,
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

  @spy_on_validate_parameters(ValidatorBase)
  def test_initialize__parameter_validation(
      self,
      validate_parameters_spy: mock.Mock,
      concrete_validator_base_instance: ValidatorBase,
  ) -> None:
    assert_parameter_schema(
        instance=concrete_validator_base_instance,
        parameter_definitions={"name": {
            "type": str
        }}
    )
    validate_parameters_spy.assert_called_once_with(
        concrete_validator_base_instance
    )
