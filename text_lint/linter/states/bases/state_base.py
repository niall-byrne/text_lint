"""StateBase class."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # no cover
  from text_lint.linter import Linter


class StateBase:
  """Base class for linter state."""

  linter: "Linter"

  def __init__(self, linter: "Linter") -> None:
    self._linter = linter

  def log(self, message: str, indent: bool = False) -> None:
    """Log a message to the console."""
    self._linter.log(message, indent=indent)
