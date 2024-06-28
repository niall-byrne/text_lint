"""ResultTree class."""

from typing import Dict, List, Optional, Tuple, Union

from text_lint.exceptions.results import SplitGroupNotFound

# A tree's value can be either:
#   - A single captured value from a regex
#   - A list created by splitting a captured value from a regex

AliasSingleAndSplitCaptures = Tuple[Union[str, List[str]], ...]
AliasTreeValue = Union[str, List[str]]
AliasRecursiveTreeResult = Dict[
    "AliasTreeValue",
    Union["AliasTreeValue", List["AliasRecursiveTreeResult"]],
]


class ResultTree:
  """Nested parsing results represented as tree."""

  def __init__(self, value: "AliasTreeValue") -> None:
    self.value = value
    self.children: List["ResultTree"] = []

  @classmethod
  def create(cls, value: "AliasTreeValue") -> "ResultTree":
    return cls(value=value)

  def __key(self) -> Tuple[str]:
    return (str(self.value),)

  def __hash__(self) -> int:
    return hash(self.__key())

  def __eq__(self, other: object) -> bool:
    if isinstance(other, ResultTree):
      return self.value == other.value
    return NotImplemented

  def add_matches(
      self,
      capture_groups: AliasSingleAndSplitCaptures,
      splits: Dict[int, Optional[str]],
      index: int = 0,
  ) -> None:
    """Add a set of capture groups to the tree."""

    for split in splits.keys():
      if split > len(capture_groups):
        raise SplitGroupNotFound(split)

    self._add_matches(
        capture_groups,
        splits,
        index,
    )

  def _add_matches(
      self, capture_groups: AliasSingleAndSplitCaptures,
      splits: Dict[int, Optional[str]], index: int
  ) -> None:
    if index < len(capture_groups):
      if index + 1 in splits:
        indexed_capture = capture_groups[index]
        # Assertion: Capture groups should not be split twice
        assert isinstance(indexed_capture, str)
        split_capture = indexed_capture.split(splits[index + 1])
        capture_groups = (
            capture_groups[:index] + (split_capture,) +
            capture_groups[index + 1:]
        )
      self._add_matches_recursive(capture_groups, splits, index)

  def _add_matches_recursive(
      self,
      capture_groups: AliasSingleAndSplitCaptures,
      splits: Dict[int, Optional[str]],
      index: int,
  ) -> None:
    nested_result = self.create(value=capture_groups[index])
    self.children.append(nested_result)
    # pylint: disable=protected-access
    nested_result._add_matches(capture_groups, splits, index + 1)

  def clone(self) -> "ResultTree":
    clone = ResultTree.create(self.value)
    clone.children = [child.clone() for child in self.children]
    return clone

  def representation(self) -> "AliasRecursiveTreeResult":
    """Return a dictionary representation of the nested tree structure."""

    return {
        "value": self.value,
        "capture": [result.representation() for result in self.children]
    }
