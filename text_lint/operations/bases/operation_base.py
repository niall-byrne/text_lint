"""OperationBase class."""

import abc
from typing import TYPE_CHECKING, Generic, TypeVar

from text_lint.operations.mixins.parameter_validation import (
    ParameterValidationMixin,
)
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states.bases.state_base import StateBase

TypeState = TypeVar("TypeState", bound="StateBase")

YAML_EXAMPLE_SECTIONS = {
    "notes_section": _("Notes"),
    "options_section": _("Options"),
}


class OperationBase(Generic[TypeState], ParameterValidationMixin, abc.ABC):

  hint: str
  internal_use_only: bool = False
  operation: str
  yaml_example: str

  @abc.abstractmethod
  def apply(
      self,
      state: "TypeState",
  ) -> None:
    """Override this method to type narrow state."""
