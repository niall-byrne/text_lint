"""OperatorBase class."""

from typing import TYPE_CHECKING, List, Optional, TypeVar

from text_lint.sequencers.patterns.loop import LoopPattern
from .sequencer_base import SequencerBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.bases.operation_base import OperationBase

TypeOperation = TypeVar("TypeOperation", bound="OperationBase")


class OperatorBase(SequencerBase[TypeOperation]):
  """A base class for iterating over discrete operations."""

  _entities: List["TypeOperation"]
  pattern: Optional[LoopPattern]
  pattern_identifier = -1

  def __init__(self, operations: List["TypeOperation"]) -> None:
    super().__init__(operations)
    self.pattern = None

  def insert(self, entities: "List[TypeOperation]", count: int) -> None:
    """Insert a sequence of operations at the current index."""

    if count == self.pattern_identifier:
      self.pattern = LoopPattern(
          start=self.index,
          end=self.index + len(entities),
      )
    else:
      if self.pattern:
        # Extend the loop's end when inserting inside it.
        self.pattern.end += len(entities)
      entities = entities * count

    self._entities = (
        self._entities[:self.index] + entities + self._entities[self.index:]
    )

  def __next__(self) -> "TypeOperation":
    if self.pattern and self.index == self.pattern.end:
      self.index = self.pattern.start
    if self.index < len(self._entities):
      operation = self.current
      self.index += 1
      return operation
    raise StopIteration
