"""ValidationBase class."""

import abc
from typing import TYPE_CHECKING

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

  @abc.abstractmethod
  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Apply the validation logic."""
