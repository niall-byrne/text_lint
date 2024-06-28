"""NoopLookup class."""

from typing import TYPE_CHECKING

from text_lint.utilities.translations import _
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE = """

- name: noop lookup example
  operation: validate_debug
  saved:
    - example.noop

"""


class NoopLookup(LookupBase):
  """NoopLookup operation for ResultForest instances."""

  hint = _("a simple no-operation")
  operation = "noop"

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """No modifications to the results or the ResultForest cursor."""
