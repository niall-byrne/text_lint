"""StateBase class."""

import abc
from typing import TYPE_CHECKING, Any, overload

if TYPE_CHECKING:  # no cover
  from text_lint.controller import Controller


class StateBase(abc.ABC):
  """Base class for linter state."""

  linter: "Controller"

  def __init__(self, linter: "Controller") -> None:
    self.linter = linter

  @overload
  def fail(self, expected: str) -> None:
    ...

  @abc.abstractmethod
  def fail(self, *args: Any, **kwargs: Any) -> None:
    """Raise an exception indicating this operation has failed."""

  def log(self, message: str, indent: bool = False) -> None:
    """Log a message to the console."""
    self.linter.log(message, indent=indent)
