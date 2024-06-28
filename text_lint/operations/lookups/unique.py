"""UniqueFilterLookup class."""

from typing import TYPE_CHECKING

from text_lint.utilities.translations import _
from .bases.lookup_base import LookupBase
from .to_unique import UniqueLookup

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: unique result lookup example
  operation: validate_debug
  saved:
    - example.capture.unique.capture

"""


class UniqueFilterLookup(LookupBase):
  """UniqueFilterLookup operation for ResultForest instances."""

  hint = _("filter unique values from the saved result")
  operation = "unique"

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Filter unique values from the saved result."""

    controller.forest.cursor.unique()

    to_unique_lookup = UniqueLookup(
        self.lookup_name,
        self.result_set,
        self.requesting_operation_name,
    )
    to_unique_lookup.apply(controller)
