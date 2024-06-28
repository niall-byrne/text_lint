"""OperatorBase class."""

from typing import TYPE_CHECKING, List, Optional, TypeVar

from text_lint.sequencers.patterns.loop import LoopPattern
from .sequencer_base import SequencerBase

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

  from text_lint.operations.bases.operation_base import OperationBase

TypeOperation = TypeVar("TypeOperation", bound="OperationBase")


class OperatorBase(SequencerBase[TypeOperation]):
  """A base class for iterating over discrete operations."""

  _entities: List["TypeOperation"]
  _patterns: List["LoopPattern"]

  def __init__(self, operations: List["TypeOperation"]) -> None:
    super().__init__(operations)
    self._patterns = []

  def insert(self, entities: "List[TypeOperation]") -> None:
    """Insert a sequence of operations at the current index."""

    self._entities = (
        self._entities[:self.index] + entities + self._entities[self.index:]
    )

  def start_repeating(self, count: int) -> None:
    """Start a repeating sequence of operations."""
    self._patterns.append(LoopPattern(
        index=self.index,
        count=count,
    ),)

  def stop_repeating(self) -> None:
    """End a repeating sequence of operations."""
    self._get_next_pattern()

  def __next__(self) -> "TypeOperation":
    if self.index < len(self._entities):
      operation = self.current
      self.index += 1
      return operation
    if self._get_next_pattern():
      return self.__next__()
    raise StopIteration

  def _get_next_pattern(self) -> Optional["LoopPattern"]:
    if self._patterns:
      pattern = self._patterns[-1]

      if pattern.count == -1:
        self.index = pattern.index
        return pattern

      if pattern.count > 1:
        pattern.count -= 1
        self._patterns[-1] = pattern
        self.index = pattern.index
        return pattern

      self._patterns.pop()
      return self._get_next_pattern()
    return None
