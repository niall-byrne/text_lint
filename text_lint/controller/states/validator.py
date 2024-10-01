"""ValidatorState class."""

from typing import TYPE_CHECKING, Any, Match, Sequence, Union

from .bases.state_base import StateBase

if TYPE_CHECKING:  # no cover
  from text_lint.controller import Controller
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

  def __init__(self, linter: "Controller") -> None:
    super().__init__(linter)
    self.operation = self.linter.validators.last

  def fail(self, *args: Any, **kwargs: Any) -> None:
    """Raise an exception indicating this operation has failed."""

  def lookup_expression(
      self,
      lookup_expression: "LookupExpression",
  ) -> "AliasLookupResult":
    """Perform the given lookup expression."""

    return self.linter.forest.lookup(
        self.linter,
        lookup_expression,
        self.operation.name,
    )

  def save(self, matches: Union[Match[str], Sequence[Match[str]]]) -> None:
    """Save the given regex match group(s)."""
