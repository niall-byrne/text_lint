"""SequencerBase class."""

import abc
from typing import Generic, Iterator, List, TypeVar

TypeSequencerEntity = TypeVar("TypeSequencerEntity")


class SequencerBase(abc.ABC, Generic[TypeSequencerEntity]):
  """A base class for iterating over discrete operations."""

  _entities: List["TypeSequencerEntity"]

  def __init__(self, entities: List["TypeSequencerEntity"]) -> None:
    self._entities = entities
    self.index = 0

  @property
  def current(self) -> "TypeSequencerEntity":
    return self._entities[self.index]

  def __iter__(self) -> Iterator["TypeSequencerEntity"]:
    return self

  @abc.abstractmethod
  def __next__(self) -> "TypeSequencerEntity":
    """Return the next entity in the sequence."""
