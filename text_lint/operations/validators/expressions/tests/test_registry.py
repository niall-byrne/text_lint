"""Test the expressions dictionary."""

import pytest
from .. import (
    Add,
    Divide,
    Exponent,
    GreaterThan,
    GreaterThanOrEqual,
    LessThan,
    LessThanOrEqual,
    Multiply,
    Subtract,
    expressions_registry,
)


class TestExpressionsRegistry:
  """Test the expressions dictionary."""

  @pytest.mark.parametrize("index", range(len(expressions_registry)))
  def test_vary_expression__returns_correct_value(
      self,
      index: int,
  ) -> None:
    expected_operations = [
        Add.operator,
        Divide.operator,
        Exponent.operator,
        GreaterThan.operator,
        GreaterThanOrEqual.operator,
        LessThan.operator,
        LessThanOrEqual.operator,
        Multiply.operator,
        Subtract.operator,
    ]
    validator_registry_key = list(expressions_registry.keys())[index]

    retrieved_validator_class = expressions_registry[validator_registry_key]

    assert retrieved_validator_class.operator == expected_operations[index]
