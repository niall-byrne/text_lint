"""ResultTreeCursor class."""

from typing import TYPE_CHECKING, List, Union

from text_lint.results.tree import ResultTree
from text_lint.utilities.collections import unique_list

if TYPE_CHECKING:  # pragma: no cover
  from .tree import ResultTree

AliasResultForestCursor = List[Union["ResultTree", "AliasResultForestCursor"]]


class ResultTreeCursor:
  """Represents a location within a ResultForest instance."""

  def __init__(self) -> None:
    self._location: "AliasResultForestCursor" = []

  def clone(self) -> "ResultTreeCursor":
    """Create a nested copy of all trees at the specified location."""
    cloned_result_tree = ResultTreeCursor()
    cloned_result_tree.location = self._cloned_location(self.location, [])
    return cloned_result_tree

  def _cloned_location(
      self,
      location: "AliasResultForestCursor",
      cloned_location: "AliasResultForestCursor",
  ) -> "AliasResultForestCursor":
    for selected_location in location:
      if isinstance(selected_location, ResultTree):
        cloned_location.append(selected_location.clone())
      if isinstance(selected_location, list):
        cloned_location.append(self._cloned_location(selected_location, []))
    return cloned_location

  @property
  def location(self) -> "AliasResultForestCursor":
    """Return the current location within the ResultForest instance."""
    return self._location

  @location.setter
  def location(
      self,
      position: "AliasResultForestCursor",
  ) -> None:
    """Reposition the cursor within the ResultForest instance."""
    self._location = position

  def flatten(self) -> None:
    """Merge the current location's tree groups."""
    flattened_location: "AliasResultForestCursor" = []
    for location in self._location:
      if isinstance(location, ResultTree):
        flattened_location.append(location)
      else:
        flattened_location += location
    self._location = flattened_location

  def increment_depth(self) -> None:
    """Increase tree depth by one set of nodes."""
    thicket: "AliasResultForestCursor" = []
    self._increment_depth_location(self._location, thicket)
    self._location = thicket

  def _increment_depth_location(
      self,
      forest: Union["ResultTree", "AliasResultForestCursor"],
      new_location: "AliasResultForestCursor",
  ) -> None:
    if isinstance(forest, ResultTree):
      new_location.append(list(forest.children))
    else:
      for woods in forest:
        self._increment_depth_location(woods, new_location)

  def unique(self) -> None:
    """Select the first unique value for each tree at the current location."""
    unique_location: "AliasResultForestCursor" = []
    for selected_location in self._location:
      self._unique_location(selected_location, unique_location)
    self._location = unique_location

  def _unique_location(
      self,
      location: "Union[ResultTree, AliasResultForestCursor]",
      unique_location: "AliasResultForestCursor",
  ) -> "AliasResultForestCursor":
    if isinstance(location, ResultTree):
      location.children = unique_list(location.children)
      if location not in unique_location:
        unique_location.append(location)
    else:
      nested_unique_location: "AliasResultForestCursor" = []
      for selected_nested_location in location:
        self._unique_location(
            selected_nested_location,
            nested_unique_location,
        )
      unique_location.append(nested_unique_location)
    return unique_location
