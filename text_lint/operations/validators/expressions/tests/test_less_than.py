"""Test the LessThan class."""
import pytest
from ..bases.expression_base import ExpressionBase
from ..less_than import LessThan


class TestLessThan:
  """Test the LessThan class."""

  test_class = LessThan

  def test_initialize__attributes(self) -> None:
    instance = self.test_class()

    assert instance.operator == "<"

  def test_initialize__inheritance(self) -> None:
    instance = self.test_class()

    assert isinstance(instance, ExpressionBase)

  @pytest.mark.parametrize(
      "input_a,input_b,expected_result",
      [
          (6.1, 3, False),
          (3, 3, False),
          (3, 6.1, True),
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
