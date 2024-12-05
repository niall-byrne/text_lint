"""NameLookup class."""

from typing import TYPE_CHECKING, Type

from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.lookups import LookupUnknown
from text_lint.operations.lookups.bases.lookup_base import LookupBase
from text_lint.operations.lookups.index import IndexLookup
from text_lint.operations.lookups.name import NameLookup
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE_COMPONENTS = (
    _("default result lookup examples"),
)
YAML_EXAMPLE = """

- name: {0}
  operation: validate_debug
  saved:
    - example1.capture(1).to_group.~specified_name
    - example2.capture(1).1
    - ~specified_name

""".format(*YAML_EXAMPLE_COMPONENTS)


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
    """Apply this operation to the given state object.

    :param state: The state object to apply this operation to.
    :raises: LookupUnknown
    """
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
