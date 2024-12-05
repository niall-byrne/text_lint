"""LookupState class."""

from typing import TYPE_CHECKING

from text_lint.exceptions.lookups import LookupFailure
from text_lint.utilities.whitespace import new_line
from .bases.state_base import StateBase

if TYPE_CHECKING:  # no cover
  from text_lint.operations.lookups.bases.lookup_base import LookupBase
  from text_lint.results.cursor import ResultTreeCursor
  from text_lint.results.forest import AliasLookupResult


class LookupState(StateBase):
  """State for lookup operations."""

  @property
  def cursor(self) -> "ResultTreeCursor":
    """Return the ResultTreeCursor instance being used to navigate results."""
    return self._linter.forest.cursor

  def fail(self, translated_description: str, operation: "LookupBase") -> None:
    """Raise an exception indicating an operation has failed.

    :param translated_description:  A translated description of the failure.
    :param operation:  The lookup operation instance that has failed.
    :raises: LookupFailure
    """
    raise LookupFailure(
        translated_description=new_line(translated_description),
        lookup=operation,
    )

  @property
  def results(self) -> "AliasLookupResult":
    """Return the lookup results."""
    return self._linter.forest.lookup_results

  @results.setter
  def results(self, value: "AliasLookupResult") -> None:
    """Set the lookup results to the given value.

    :param value: The value to assign as the lookup results.
    """
    self._linter.forest.lookup_results = value
