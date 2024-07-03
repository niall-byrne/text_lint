"""OperationBase class."""

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller


class OperationBase(abc.ABC):
  """Text file operation base class."""

  hint: str
  operation: str
  yaml_example: str

  @abc.abstractmethod
  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Base method for applying an operation."""
