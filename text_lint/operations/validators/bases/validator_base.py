"""ValidationBase class."""

import abc
import sys
from typing import TYPE_CHECKING, Any

from text_lint.config import NEW_LINE
from text_lint.operations.bases.operation_base import OperationBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller


class ValidationBase(
    OperationBase,
    abc.ABC,
):
  """Parser validation base class."""

  operation: str
  hint: str

  def __init__(self, name: str) -> None:
    self.name = name

  def print(self, message: Any) -> None:
    """Write a message to the console."""
    sys.stdout.write(message + NEW_LINE)

  @abc.abstractmethod
  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Apply the validation logic."""
