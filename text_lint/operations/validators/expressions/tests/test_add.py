"""Test the Add class."""

import pytest
from ..add import Add
from ..bases.expression_base import ExpressionBase


class TestAdd:
  """Test the Add class."""

  test_class = Add

  def test_initialize__attributes(self) -> None:
    instance = self.test_class()

    assert instance.operator == "+"

  def test_initialize__inheritance(self) -> None:
    instance = self.test_class()

    assert isinstance(instance, ExpressionBase)

  @pytest.mark.parametrize(
      "input_a,input_b,expected_result",
      [
          (6, 3, 9),
          (2.7, 6.3, 9),
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
