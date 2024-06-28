"""CaptureLookup class."""

from typing import TYPE_CHECKING, List, Union

from text_lint.results.tree import ResultTree
from text_lint.utilities.translations import _
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller
  from text_lint.results.tree import AliasRecursiveTreeResult

YAML_EXAMPLE = """

- name: capture group result lookup example
  operation: validate_debug
  saved:
    - example.capture

note: to access other regex capture groups, simply chain this operation:
        - example.capture.capture             # 2nd regex capture group
        - example.capture.capture.capture     # 3rd regex capture group

"""

AliasRecursiveForestLocation = Union[
    ResultTree,
    List[Union["ResultTree", 'AliasRecursiveForestLocation']],
]


class CaptureLookup(LookupBase):
  """CaptureLookup operation for ResultForest instances."""

  hint = _("select the next capture group of the saved result")
  operation = "capture"

  def _retrieve_next_capture_group(
      self,
      forest_location: "AliasRecursiveForestLocation",
      thicket: List[Union[List[str], "AliasRecursiveTreeResult"]],
  ) -> None:
    if isinstance(forest_location, ResultTree):
      thicket.append([tree.value for tree in forest_location.children])
    else:
      for grove in forest_location:
        self._retrieve_next_capture_group(grove, thicket)

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Select all next capture group from the current ResultForest location."""

    controller.forest.lookup_results = []

    self._retrieve_next_capture_group(
        controller.forest.cursor.location,
        controller.forest.lookup_results,
    )

    controller.forest.cursor.traverse()
