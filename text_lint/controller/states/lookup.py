"""LookupState class."""

from typing import TYPE_CHECKING, Any

from .bases.state_base import StateBase

if TYPE_CHECKING:  # no cover
  from text_lint.results.cursor import (
      AliasResultForestCursor,
      ResultTreeCursor,
  )
  from text_lint.results.forest import AliasLookupResult


class LookupState(StateBase):
  """State for lookup operations."""

  def fail(self, *args: Any, **kwargs: Any) -> None:
    """Raise an exception indicating this operation has failed."""

  @property
  def results(self) -> "AliasLookupResult":
    return self.linter.forest.lookup_results

  @results.setter
  def results(self, value: "AliasLookupResult") -> None:
    self.linter.forest.lookup_results = value

  @property
  def cursor(self) -> "ResultTreeCursor":
    return self.linter.forest.cursor

  @cursor.setter
  def cursor(self, location: "AliasResultForestCursor") -> None:
    self.linter.forest.cursor.location = location
