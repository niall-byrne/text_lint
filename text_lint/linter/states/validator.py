"""ValidatorState class."""

from typing import TYPE_CHECKING

from text_lint.exceptions.validators import ValidationFailure
from text_lint.utilities.whitespace import new_line
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
  from text_lint.results.tree import ResultTree


class ValidatorState(StateBase):
  """State for validator operations."""

  operation: "ValidatorBase"

  def __init__(self, linter: "Linter") -> None:
    super().__init__(linter)
    self.operation = self._linter.validators.last

  def fail(
      self,
      translated_description: str,
      translated_detail: str,
  ) -> None:
    """Raise an exception indicating an operation has failed."""

    raise ValidationFailure(
        description=new_line(translated_description),
        detail=new_line(translated_detail),
        validator=self.operation
    )

  def lookup_expression(
      self,
      lookup_expression: "LookupExpression",
  ) -> "AliasLookupResult":
    """Perform the given lookup expression."""

    return self._linter.forest.lookup_expression(
        self._linter,
        lookup_expression,
    )

  def save(self, tree: "ResultTree") -> None:
    """Save the given result tree."""

    self._linter.forest.add(tree)
