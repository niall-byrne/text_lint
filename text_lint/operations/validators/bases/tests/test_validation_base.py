"""Test the ValidationBase class."""

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.config import NEW_LINE
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
        "yaml_example": "mocked_yaml_example",
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

  @pytest.mark.parametrize("mocked_message", ("message1", "message2"))
  def test_print__vary_message__writes_to_stdout(
      self,
      concrete_validator_base_instance: ValidationBase,
      capfd: pytest.CaptureFixture[str],
      mocked_message: str,
  ) -> None:
    concrete_validator_base_instance.print(mocked_message)

    stdout, stderr = capfd.readouterr()
    assert stdout == mocked_message + NEW_LINE
    assert stderr == ""
