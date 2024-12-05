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
    """Initialize ResultTree instances.

    :param value: The root value of the new ResultTree.
    """
    self.value = value
    self.children: List["ResultTree"] = []

  @classmethod
  def create(cls, value: "AliasTreeValue") -> "ResultTree":
    """Create a new ResultTree instance.

    :param value: The root value of the new ResultTree.
    :returns: The created tree.
    """
    return cls(value=value)

  def __key(self) -> Tuple[str]:
    return (str(self.value),)

  def __hash__(self) -> int:
    """Implement hashing for ResultTree instances.

    :returns: The hashed value of this tree.
    """
    return hash(self.__key())

  def __eq__(self, other: object) -> bool:
    """Implement the equality operator for ResultTree instances.

    :param other: The other object to compare to this ResultTree instance.
    :returns: A boolean for whether this tree is equal to the specified tree.
    :raises: NotImplemented
    """
    if isinstance(other, ResultTree):
      return self.value == other.value
    return NotImplemented

  def add_matches(
      self,
      capture_groups: AliasSingleAndSplitCaptures,
      splits: Dict[int, Optional[str]],
      index: int = 0,
  ) -> None:
    """Add a set of capture groups to the tree.

    :param capture_groups: A tuple of values captured from assertion regexes.
    :param splits: A dictionary of splits to perform on the captured values.
    :param index: The index of the current captured value being processed.
    """
    for split in splits.keys():
      if split > len(capture_groups):
        raise SplitGroupNotFound(split)

    self._add_matches(
        capture_groups,
        splits,
        index,
    )

  def _add_matches(
      self,
      capture_groups: AliasSingleAndSplitCaptures,
      splits: Dict[int, Optional[str]],
      index: int,
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
    """Generate a separate copy of this tree.

    :returns: The cloned tree instance.
    """
    clone = ResultTree.create(self.value)
    clone.children = [child.clone() for child in self.children]
    return clone

  def representation(self) -> "AliasRecursiveTreeResult":
    """Return a dictionary representation of the nested tree structure.

    :returns: A dictionary representation of this tree.
    """
    return {
        "value": self.value,
        "capture": [result.representation() for result in self.children]
    }
