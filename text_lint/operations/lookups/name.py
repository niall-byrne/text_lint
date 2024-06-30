"""NameLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.lookups import LookupFailure
from text_lint.results.tree import ResultTree
from text_lint.utilities.translations import _, f
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: name result lookup example
  operation: validate_debug
  saved:
    - example.capture.~specified_name.capture

"""


class NameLookup(LookupBase):
  """NameLookup operation for ResultForest instances."""

  hint = _("select a named entry from the saved result")
  operation = "name"

  msg_fmt_failure_description = _("Could not find the specified entry.")

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Select the specified tree from the current ResultForest location."""

    controller.forest.cursor.flatten()

    for tree in controller.forest.cursor.location:
      if isinstance(tree, ResultTree):
        if LOOKUP_STATIC_VALUE_MARKER + tree.value == self.lookup_name:
          controller.forest.cursor.location = [tree]
          controller.forest.lookup_results = [[tree.value]]
          break
    else:
      raise LookupFailure(
          description=f(self.msg_fmt_failure_description, nl=1),
          lookup=self,
      )
