"""Test the Exponent class."""

import pytest
from ..bases.expression_base import ExpressionBase
from ..exponent import Exponent


class TestExponent:
  """Test the Exponent class."""

  test_class = Exponent

  def test_initialize__attributes(self) -> None:
    instance = self.test_class()

    assert instance.operator == "^"

  def test_initialize__inheritance(self) -> None:
    instance = self.test_class()

    assert isinstance(instance, ExpressionBase)

  @pytest.mark.parametrize(
      "input_a,input_b,expected_result",
      [
          (2, 6, 64),
          (4, -1, 0.25),
      ],
      ids=lambda p: "'" + str(p) + "'",
  )
  def test_apply__returns_correct_results(
      self,
      input_a: float,
      input_b: float,
      expected_result: float,
  ) -> None:
    instance = self.test_class()

    result = instance.apply(input_a, input_b)

    assert result == expected_result
