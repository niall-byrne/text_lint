"""TextfileSequencer class."""

import re
from typing import TYPE_CHECKING, Optional, Pattern

from .bases.sequencer_base import SequencerBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.schema import Schema


class TextFileSequencer(SequencerBase[str]):
  """Iterator that returns the lines of a generic text file."""

  _comment_regex: Optional[Pattern[str]] = None

  def __init__(self, makefile_path: str) -> None:
    with open(makefile_path, "r", encoding='utf-8') as fh:
      super().__init__(fh.readlines())

    self.path = makefile_path

  def configure(self, schema: "Schema") -> None:
    """Apply schema configuration to the text file."""
    if schema.settings.comment_regex:
      self._comment_regex = re.compile(schema.settings.comment_regex, re.DOTALL)

  def __next__(self) -> str:
    if self.index < len(self._entities):
      next_line = self.current
      self.index += 1
      if self._is_comment(next_line):
        return self.__next__()
      return next_line
    raise StopIteration

  def _is_comment(self, next_line: str) -> bool:
    if self._comment_regex:
      return re.match(self._comment_regex, next_line) is not None
    return False
