"""NoopLookup class."""

from typing import TYPE_CHECKING

from text_lint.utilities.translations import _
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: noop result lookup example
  operation: validate_debug
  saved:
    - example.noop

"""


class NoopLookup(LookupBase):
  """NoopLookup operation for ResultForest instances."""

  hint = _("a simple no-operation")
  internal_use_only = True
  operation = "noop"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """No modifications to the results or the ResultForest cursor."""
