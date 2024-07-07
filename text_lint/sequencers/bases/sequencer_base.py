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
  """A base class for iterating over discrete operations."""

  _entities: List["TypeSequencerEntity"]
  pattern: "SequencerPatternBase"

  def __init__(self, entities: List["TypeSequencerEntity"]) -> None:
    self._entities = entities
    self.index = 0
    self.pattern = LinearPattern()

  def __len__(self) -> int:
    return len(self._entities)

  @property
  def current(self) -> "TypeSequencerEntity":
    return self._entities[self.index]

  def __iter__(self) -> Iterator["TypeSequencerEntity"]:
    return self

  def next(self) -> None:
    """Advance the index."""
    self.pattern.increment(self)

  @abc.abstractmethod
  def __next__(self) -> "TypeSequencerEntity":
    """Return the next entity in the sequence."""
