"""ValidatorState class."""

from typing import TYPE_CHECKING

from .bases.state_base import StateBase

if TYPE_CHECKING:  # no cover
  from text_lint.linter import Linter
  from text_lint.operations.validators.args.lookup_expression import (
      LookupExpression,
  )
  from text_lint.operations.validators.bases.validator_base import (
      ValidatorBase,
  )
  from text_lint.results.forest import AliasLookupResult


class ValidatorState(StateBase):
  """State for validator operations."""

  operation: "ValidatorBase"

  def __init__(self, linter: "Linter") -> None:
    super().__init__(linter)
    self.operation = self._linter.validators.last

  def lookup_expression(
      self,
      lookup_expression: "LookupExpression",
  ) -> "AliasLookupResult":
    """Perform the given lookup expression."""

    return self._linter.forest.lookup_expression(
        self._linter,
        lookup_expression,
    )
