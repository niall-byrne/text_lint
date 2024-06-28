"""OperationBase class."""

import abc
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states.bases.state_base import StateBase

TypeState = TypeVar("TypeState", bound="StateBase")


class OperationBase(Generic[TypeState], abc.ABC):

  hint: str
  operation: str

  @abc.abstractmethod
  def apply(
      self,
      state: "TypeState",
  ) -> None:
    """Override this method to type narrow state."""
