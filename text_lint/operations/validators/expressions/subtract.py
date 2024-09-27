"""Subtract class."""
from typing import Union

from .bases import expression_base


class Subtract(expression_base.ExpressionBase):
  """Subtract one value from another."""

  operator = "-"

  def apply(self, value_a: float, value_b: float) -> Union[float, bool]:
    """Apply the mathematical operator to these two values."""

    return value_a - value_b
