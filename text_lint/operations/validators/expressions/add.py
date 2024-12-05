"""Add class."""
from typing import Union

from text_lint.operations.validators.expressions.bases import expression_base


class Add(expression_base.ExpressionBase):
  """Add two values together."""

  operator = "+"

  def apply(self, value_a: float, value_b: float) -> Union[float, bool]:
    """Apply the mathematical operator to these two values."""
    return value_a + value_b
