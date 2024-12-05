"""SequencerBase class."""

import abc
from typing import TYPE_CHECKING, Generic, Iterator, List, TypeVar

from text_lint.sequencers.patterns.linear import LinearPattern

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.sequencers.patterns.bases.pattern_base import (
      SequencerPatternBase,
  )

TypeSequencerEntity = TypeVar("TypeSequencerEntity")


class SequencerBase(abc.ABC, Generic[TypeSequencerEntity]):
  """A base class for iterating over discrete entities."""

  _entities: List["TypeSequencerEntity"]
  pattern: "SequencerPatternBase"

  def __init__(self, entities: List["TypeSequencerEntity"]) -> None:
    """Initialize OperatorBase instances.

    :param entities: The objects this sequencer iterates over.
    """
    self._entities = entities
    self.index = 0
    self.pattern = LinearPattern()

  def __len__(self) -> int:
    """Implement the len operator for SequencerBase instances.

    :returns: The number of entities in this instance.
    """
    return len(self._entities)

  @property
  def current(self) -> "TypeSequencerEntity":
    """Current entity the sequencer is pointing to."""
    return self._entities[self.index]

  @property
  def last(self) -> "TypeSequencerEntity":
    """Last entity in the sequencer."""
    return self._entities[self.index - 1]

  def __iter__(self) -> Iterator["TypeSequencerEntity"]:
    """Implement the iter operation for SequencerBase instances.

    :returns: The sequencer instance itself.
    """
    return self

  def next(self) -> None:
    """Advance the sequencer to the next entity."""
    self.pattern.increment(self)

  @abc.abstractmethod
  def __next__(self) -> "TypeSequencerEntity":
    """Implement the next operation for SequencerBase instances.

    :returns: The next entity in the sequencer.
    """
