"""ValidatorBase class."""

import abc
from typing import TYPE_CHECKING

from text_lint.operations.bases.operation_base import OperationBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter import states


class ValidatorBase(
    OperationBase["states.ValidatorState"],
    abc.ABC,
):
  """Validation operation base class."""

  operation: str
  hint: str

  def __init__(self, name: str) -> None:
    self.name = name

  @abc.abstractmethod
  def apply(
      self,
      state: "states.ValidatorState",
  ) -> None:
    """Base method for applying a validator."""
