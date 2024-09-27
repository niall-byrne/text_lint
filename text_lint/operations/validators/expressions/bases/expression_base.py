"""ExpressionBase class."""

import abc
from typing import Union


class ExpressionBase(abc.ABC):
  """Base class for mathematical expressions."""

  operator: str

  @abc.abstractmethod
  def apply(self, value_a: float, value_b: float) -> Union[float, bool]:
    """Apply the mathematical operator to these two values."""
