"""Exponent class."""
from typing import Union

from .bases import expression_base


class Exponent(expression_base.ExpressionBase):
  """Apply the exponent to a value of another."""

  operator = "^"

  def apply(self, value_a: float, value_b: float) -> Union[float, bool]:
    """Apply the mathematical operator to these two values."""

    return float(value_a**value_b)
