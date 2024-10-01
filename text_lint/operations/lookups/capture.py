"""CaptureLookup class."""

from typing import TYPE_CHECKING, List, Union

from text_lint.results.tree import ResultTree
from text_lint.utilities.translations import _
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller.states import LookupState
  from text_lint.results.forest import AliasLookupResult

YAML_EXAMPLE = """

- name: capture group lookup example
  operation: validate_debug
  saved:
    - example.capture

note: To access other regex capture groups, simply chain this operation:
    - example.capture.capture             # 2nd regex capture group
    - example.capture.capture.capture     # 3rd regex capture group

"""

AliasRecursiveForestLocation = Union[
    ResultTree,
    List[Union["ResultTree", 'AliasRecursiveForestLocation']],
]


class CaptureLookup(LookupBase):
  """CaptureLookup operation for ResultForest instances."""

  hint = _("select the next capture group of a save id")
  is_positional = True
  operation = "capture"

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Select all next capture group from the current ResultForest location."""

    state.results = []

    self._update_results(
        state.cursor.location,
        state.results,
    )

    self._update_location(state)

  def _update_location(
      self,
      state: "LookupState",
  ) -> None:
    state.cursor.increment_depth()

  def _update_results(
      self,
      forest_location: "AliasRecursiveForestLocation",
      thicket: List["AliasLookupResult"],
  ) -> None:
    if isinstance(forest_location, ResultTree):
      thicket.append([tree.value for tree in forest_location.children])
    if isinstance(forest_location, list):
      for grove in forest_location:
        self._update_results(grove, thicket)
