"""Linter states for various operations."""

from typing import TYPE_CHECKING

from .assertion import AssertionState
from .lookup import LookupState
from .validator import ValidatorState

if TYPE_CHECKING:  # no cover
  from text_lint.linter import Linter


class StateFactory:
  """Encapsulate a linter instance as a state object."""

  def __init__(self, linter: "Linter") -> None:
    """Initialize StateFactory instances.

    :param linter:  The linter instance being encapsulated.
    """
    self._linter = linter

  def assertion(self) -> AssertionState:
    """Generate state for assertion operations.

    :returns: The generated state object.
    """
    return AssertionState(self._linter)

  def lookup(self) -> LookupState:
    """Generate state for lookup operations.

    :returns: The generated state object.
    """
    return LookupState(self._linter)

  def validator(self) -> ValidatorState:
    """Generate state for validator operations.

    :returns: The generated state object.
    """
    return ValidatorState(self._linter)
