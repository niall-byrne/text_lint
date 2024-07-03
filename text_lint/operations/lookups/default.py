"""NameLookup class."""

from typing import TYPE_CHECKING, Type

from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.lookups import LookupUnknown
from text_lint.utilities.translations import _
from .bases.lookup_base import LookupBase
from .index import IndexLookup
from .name import NameLookup

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: default result lookup examples
  operation: validate_debug
  saved:
    - example1.capture.~specified_name.capture
    - example2.capture.1.capture

"""


class DefaultLookup(LookupBase):
  """Default operation for unknown lookups on the ResultForest instances."""

  hint = _("handler for unknown lookups which may be result values or indexes")
  operation = "default"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Handle unknown lookups by selecting a LookupBase subclass."""
    lookup_class: Type[LookupBase]

    if self.lookup_name.isdigit():
      lookup_class = IndexLookup
    elif self.lookup_name.startswith(LOOKUP_STATIC_VALUE_MARKER):
      lookup_class = NameLookup
    else:
      raise LookupUnknown(lookup=self)

    lookup_instance = lookup_class(
        self.lookup_name,
        self.result_set,
        self.requesting_operation_name,
    )
    lookup_instance.apply(controller)
