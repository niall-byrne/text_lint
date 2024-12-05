"""OperatorBase class."""

from typing import TYPE_CHECKING, List, TypeVar

from text_lint.config import LOOP_COUNT
from text_lint.sequencers.bases.sequencer_base import SequencerBase
from text_lint.sequencers.patterns.loop import LinearLoopPattern

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

  from text_lint.operations.bases.operation_base import OperationBase

TypeOperation = TypeVar("TypeOperation", bound="OperationBase[Any]")


class OperatorBase(SequencerBase[TypeOperation]):
  """A base class for iterating over discrete operations."""

  _entities: List["TypeOperation"]

  def __init__(self, operations: List["TypeOperation"]) -> None:
    """Initialize OperatorBase instances.

    :param operations: The operations this sequencer iterates over.
    """
    super().__init__(operations)

  def insert(self, entities: "List[TypeOperation]", count: int) -> None:
    """Insert a sequence of operations at the current index.

    :param entities: The operations to insert into the sequencer.
    :param count: The number of times these new operations repeat.
    """
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
    """Return the next operation in the sequence."""
    previous_index = self.index
    self.next()
    return self._entities[previous_index]
