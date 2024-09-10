"""NameLookup class."""

from typing import TYPE_CHECKING, Type

from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.lookups import LookupUnknown
from text_lint.utilities.translations import _
from .bases.lookup_base import LookupBase
from .index import IndexLookup
from .name import NameLookup

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE = """

- name: default result lookup examples
  operation: validate_debug
  saved:
    - example1.capture().to_group.~specified_name
    - example2.capture().1
    - ~specified_name

"""


class DefaultLookup(LookupBase):
  """Default operation for unknown lookups on the ResultForest instances."""

  hint = _(
      "handler for unknown lookups which may be static values or indexes"
  )
  internal_use_only = True
  operation = "default"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      state: "LookupState",
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
        self.lookup_expression,
        self.lookup_params,
        self.requesting_operation_name,
    )
    lookup_instance.apply(state)
