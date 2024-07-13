"""Test the validator_registry dictionary."""

import pytest
from .. import ValidateDebug, ValidateEqual, validator_registry


class TestValidatorRegistry:
  """Test the validator_registry dictionary."""

  @pytest.mark.parametrize("index", range(len(validator_registry)))
  def test_vary_validator__returns_correct_value(
      self,
      index: int,
  ) -> None:
    expected_operations = [
        ValidateDebug.operation,
        ValidateEqual.operation,
    ]
    validator_registry_key = list(validator_registry.keys())[index]

    retrieved_validator_class = validator_registry[validator_registry_key]

    assert retrieved_validator_class.operation == expected_operations[index]
