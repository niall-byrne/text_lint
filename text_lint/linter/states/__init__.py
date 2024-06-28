"""Linter states for various operations."""

from typing import TYPE_CHECKING

from .assertion import AssertionState
from .lookup import LookupState
from .validator import ValidatorState

if TYPE_CHECKING:  # no cover
  from text_lint.linter import Linter


class StateFactory:
  """Encapsulate a linter instance as a state object."""

  def __init__(self, linter: "Linter"):
    self._linter = linter

  def assertion(self) -> AssertionState:
    return AssertionState(self._linter)

  def lookup(self) -> LookupState:
    return LookupState(self._linter)

  def validator(self) -> ValidatorState:
    return ValidatorState(self._linter)
