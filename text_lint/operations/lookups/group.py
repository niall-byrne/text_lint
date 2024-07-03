"""GroupLookup class."""

from itertools import chain
from typing import TYPE_CHECKING

from text_lint.utilities.translations import _
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: group result lookup example
  operation: validate_debug
  saved:
    - example.capture.group

"""


class GroupLookup(LookupBase):
  """GroupLookup operation for ResultForest instances."""

  hint = _("group the currently selected values of the saved result")
  operation = "group"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Group all trees from the current ResultForest location."""

    controller.forest.lookup_results = [
        list(chain.from_iterable(controller.forest.lookup_results))
    ]

    controller.forest.cursor.flatten()
