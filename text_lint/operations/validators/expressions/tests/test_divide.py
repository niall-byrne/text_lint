"""Test the Divide class."""

import pytest
from ..bases.expression_base import ExpressionBase
from ..divide import Divide


class TestDivide:
  """Test the Divide class."""

  test_class = Divide

  def test_initialize__attributes(self) -> None:
    instance = self.test_class()

    assert instance.operator == "/"

  def test_initialize__inheritance(self) -> None:
    instance = self.test_class()

    assert isinstance(instance, ExpressionBase)

  @pytest.mark.parametrize(
      "input_a,input_b,expected_result",
      [
          (6, 3, 2),
          (7, 2, 3.5),
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
