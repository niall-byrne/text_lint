"""Linter recursion detection class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOP_RECURSION_LIMIT
from text_lint.exceptions.linter import LinterRecursionLimitExceeded

if TYPE_CHECKING:  # no cover
  from text_lint.linter import Linter


class RecursionDetection:
  """Linter recursion detector."""

  def __init__(self, linter: "Linter") -> None:
    """Initialize RecursionDetection instances.

    :param linter:  The linter instance being monitored.
    """
    self._linter = linter
    self.index = -1
    self.count = 0

  def detect(self) -> None:
    """Detect whether the linter has reached the recursion limit.

    :raises: LinterRecursionLimitExceeded
    """
    if self._linter.textfile.index != self.index:
      self.count = 0
    if self._linter.textfile.index == self.index:
      self.count += 1
    if self.count > LOOP_RECURSION_LIMIT:
      raise LinterRecursionLimitExceeded(linter=self._linter)
    self.index = self._linter.textfile.index
