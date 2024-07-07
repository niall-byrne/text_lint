"""OperatorBase class."""

from typing import TYPE_CHECKING, List, TypeVar

from text_lint.config import LOOP_COUNT
from text_lint.sequencers.patterns.loop import LinearLoopPattern
from .sequencer_base import SequencerBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.bases.operation_base import OperationBase

TypeOperation = TypeVar("TypeOperation", bound="OperationBase")


class OperatorBase(SequencerBase[TypeOperation]):
  """A base class for iterating over discrete operations."""

  _entities: List["TypeOperation"]

  def __init__(self, operations: List["TypeOperation"]) -> None:
    super().__init__(operations)

  def insert(self, entities: "List[TypeOperation]", count: int) -> None:
    """Insert a sequence of operations at the current index."""

    if count == LOOP_COUNT:
      self.pattern = LinearLoopPattern(
          start=self.index,
          end=self.index + len(entities),
      )
    else:
      self.pattern.adjust(len(entities))
      entities = entities * count

    self._entities = (
        self._entities[:self.index] + entities + self._entities[self.index:]
    )

  def __next__(self) -> "TypeOperation":
    previous_index = self.index
    self.next()
    return self._entities[previous_index]
