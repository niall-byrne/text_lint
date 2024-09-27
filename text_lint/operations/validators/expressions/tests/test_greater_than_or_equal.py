"""Test the GreaterThanOrEqual class."""
import pytest
from ..bases.expression_base import ExpressionBase
from ..greater_than_or_equal import GreaterThanOrEqual


class TestGreaterThanOrEqual:
  """Test the GreaterThanOrEqual class."""

  test_class = GreaterThanOrEqual

  def test_initialize__attributes(self) -> None:
    instance = self.test_class()

    assert instance.operator == ">="

  def test_initialize__inheritance(self) -> None:
    instance = self.test_class()

    assert isinstance(instance, ExpressionBase)

  @pytest.mark.parametrize(
      "input_a,input_b,expected_result",
      [
          (6.1, 3, True),
          (3, 3, True),
          (3, 6.1, False),
      ],
      ids=lambda p: "'" + str(p) + "'",
  )
  def test_apply__returns_correct_results(
      self,
      input_a: float,
      input_b: float,
      expected_result: bool,
  ) -> None:
    instance = self.test_class()

    result = instance.apply(input_a, input_b)

    assert result == expected_result
