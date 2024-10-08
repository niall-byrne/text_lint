"""ResultTree class."""

from typing import Dict, List, Optional, Tuple, Union

AliasRecursiveTreeResult = Dict[
    str,
    Union[str, Tuple["AliasRecursiveTreeResult", ...]],
]


class ResultTree:
  """Nested parsing results represented as tree."""

  def __init__(self, value: str) -> None:
    self.value = value
    self.children: List["ResultTree"] = []

  @classmethod
  def create(cls, value: str) -> "ResultTree":
    return cls(value=value)

  def __key(self) -> Tuple[str]:
    return (self.value,)

  def __hash__(self) -> int:
    return hash(self.__key())

  def __eq__(self, other: object) -> bool:
    if isinstance(other, ResultTree):
      return self.value == other.value
    return NotImplemented

  def add_matches(
      self,
      capture_groups: Tuple[str, ...],
      splits: Dict[int, Optional[str]],
      index: int = 0,
  ) -> None:
    """Add a set of capture groups to the tree."""

    if index < len(capture_groups):
      if index + 1 in splits:
        self.add_matches(capture_groups[:index], splits, index + 1)
        self._add_matches_split(capture_groups[index], splits[index + 1])
        self.add_matches(capture_groups[index:], splits, index + 1)
      else:
        self._add_matches_recursive(capture_groups, splits, index)

  def _add_matches_split(
      self,
      capture_group: str,
      separator: Optional[str],
  ) -> None:
    for split_group in capture_group.split(separator):
      self.children.append(self.create(value=split_group))

  def _add_matches_recursive(
      self,
      capture_groups: Tuple[str, ...],
      splits: Dict[int, Optional[str]],
      index: int,
  ) -> None:
    nested_result = self.create(value=capture_groups[index])
    self.children.append(nested_result)
    nested_result.add_matches(capture_groups, splits, index + 1)

  def clone(self) -> "ResultTree":
    clone = ResultTree.create(self.value)
    clone.children = [child.clone() for child in self.children]
    return clone

  def representation(self) -> "AliasRecursiveTreeResult":
    """Return a dictionary representation of the nested tree structure."""

    return {
        "value": self.value,
        "children": tuple(result.representation() for result in self.children)
    }
