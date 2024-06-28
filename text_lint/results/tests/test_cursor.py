"""Test the ResultTreeCursor class."""

from typing import Any, List, Tuple

from ..cursor import ResultTreeCursor
from ..tree import ResultTree


class TestResultTreeCursor:
  """Test the ResultTreeCursor class."""

  def assert_cursor_length(self, cursor: Any, length: int) -> None:
    assert isinstance(cursor.location, list)
    assert len(cursor.location) == length

  def select_asserted_result_tree(
      self,
      location: Any,
      value: str,
      child_values: List[str],
  ) -> Tuple[ResultTree, List[ResultTree]]:
    assert isinstance(location, ResultTree)
    assert location.value == value
    assert len(location.children) == len(child_values)
    for index, child_value in enumerate(child_values):
      assert location.children[index].value == child_value

    return location, location.children

  def select_asserted_list_of_result_trees(
      self,
      location: Any,
      length: int,
  ) -> List[ResultTree]:
    assert isinstance(location, list)
    assert len(location) == length
    assert isinstance(location[0], ResultTree)

    return location

  def test_initialize__attributes(
      self,
      result_tree_cursor_instance: ResultTreeCursor,
  ) -> None:
    assert result_tree_cursor_instance.location == []

  def test_clone__single_tree__single_group__creates_independent_copy(
      self,
      result_tree_cursor_instance: ResultTreeCursor,
  ) -> None:
    mocked_tree = ResultTree(value="A")
    mocked_tree.children = [ResultTree(value="B"), ResultTree(value="B")]
    result_tree_cursor_instance.location.append(mocked_tree)

    cloned_cursor = result_tree_cursor_instance.clone()

    self.assert_cursor_length(cloned_cursor, length=1)
    cloned_tree, cloned_children = self.select_asserted_result_tree(
        cloned_cursor.location[0],
        value="A",
        child_values=["B", "B"],
    )
    assert cloned_tree is not mocked_tree
    assert cloned_children[0] is not mocked_tree.children[0]
    assert cloned_children[0] is not mocked_tree.children[1]
    assert cloned_children[1] is not mocked_tree.children[0]
    assert cloned_children[1] is not mocked_tree.children[1]

  def test_clone__two_trees__two_groups__creates_independent_copy(
      self,
      result_tree_cursor_instance: ResultTreeCursor,
  ) -> None:
    mocked_tree1 = ResultTree(value="A")
    mocked_tree1.children = [ResultTree(value="B"), ResultTree(value="B")]
    mocked_tree2 = ResultTree(value="C")
    mocked_tree2.children = [ResultTree(value="D"), ResultTree(value="D")]
    result_tree_cursor_instance.location.append([mocked_tree1])
    result_tree_cursor_instance.location.append([mocked_tree2])

    cloned_cursor = result_tree_cursor_instance.clone()

    self.assert_cursor_length(cloned_cursor, length=2)
    selected_list1 = self.select_asserted_list_of_result_trees(
        cloned_cursor.location[0],
        length=1,
    )

    cloned_tree1, cloned_children1 = self.select_asserted_result_tree(
        selected_list1[0],
        value="A",
        child_values=["B", "B"],
    )
    assert cloned_tree1 is not mocked_tree1
    assert (
        cloned_children1[0] is not mocked_tree1.children[0]
        or mocked_tree1.children[1]
    )
    assert (
        cloned_children1[1] is not mocked_tree1.children[0]
        or mocked_tree1.children[1]
    )

    selected_list2 = self.select_asserted_list_of_result_trees(
        cloned_cursor.location[1], length=1
    )
    cloned_tree2, cloned_children2 = self.select_asserted_result_tree(
        selected_list2[0],
        value="C",
        child_values=["D", "D"],
    )
    assert cloned_tree2 is not mocked_tree2
    assert (
        cloned_children2[0] is not mocked_tree2.children[0]
        or mocked_tree2.children[1]
    )
    assert (
        cloned_children2[1] is not mocked_tree2.children[0]
        or mocked_tree2.children[1]
    )

  def test_flatten__single_tree__single_group__merges_location(
      self,
      result_tree_cursor_instance: ResultTreeCursor,
  ) -> None:
    mocked_tree = ResultTree(value="A")
    mocked_tree.children = [ResultTree(value="B"), ResultTree(value="B")]
    result_tree_cursor_instance.location.append(mocked_tree)

    result_tree_cursor_instance.flatten()

    self.assert_cursor_length(result_tree_cursor_instance, length=1)
    self.select_asserted_list_of_result_trees(
        result_tree_cursor_instance.location,
        length=1,
    )
    self.select_asserted_result_tree(
        result_tree_cursor_instance.location[0],
        value="A",
        child_values=["B", "B"],
    )

  def test_flatten__two_trees__two_groups__merges_location(
      self,
      result_tree_cursor_instance: ResultTreeCursor,
  ) -> None:
    mocked_tree = ResultTree(value="A")
    mocked_tree.children = [ResultTree(value="B"), ResultTree(value="B")]
    result_tree_cursor_instance.location.append([mocked_tree, mocked_tree])

    result_tree_cursor_instance.flatten()

    self.assert_cursor_length(result_tree_cursor_instance, length=2)
    self.select_asserted_list_of_result_trees(
        result_tree_cursor_instance.location,
        length=2,
    )
    self.select_asserted_result_tree(
        result_tree_cursor_instance.location[0],
        value="A",
        child_values=["B", "B"],
    )
    self.select_asserted_result_tree(
        result_tree_cursor_instance.location[1],
        value="A",
        child_values=["B", "B"],
    )

  def test_increment_depth__single_tree__selects_children(
      self,
      result_tree_cursor_instance: ResultTreeCursor,
  ) -> None:
    mocked_tree = ResultTree(value="A")
    mocked_tree.children = [ResultTree(value="B"), ResultTree(value="B")]
    result_tree_cursor_instance.location.append(mocked_tree)

    result_tree_cursor_instance.increment_depth()

    self.assert_cursor_length(result_tree_cursor_instance, length=1)
    selected_list = self.select_asserted_list_of_result_trees(
        result_tree_cursor_instance.location[0],
        length=2,
    )
    self.select_asserted_result_tree(
        selected_list[0],
        value="B",
        child_values=[],
    )
    self.select_asserted_result_tree(
        selected_list[1],
        value="B",
        child_values=[],
    )

  def test_increment_depth__two_trees__selects_children(
      self,
      result_tree_cursor_instance: ResultTreeCursor,
  ) -> None:
    mocked_tree1 = ResultTree(value="A")
    mocked_tree1.children = [ResultTree(value="B"), ResultTree(value="B")]
    mocked_tree2 = ResultTree(value="C")
    mocked_tree2.children = [ResultTree(value="D"), ResultTree(value="D")]
    result_tree_cursor_instance.location.append([mocked_tree1, mocked_tree2])

    result_tree_cursor_instance.increment_depth()

    self.assert_cursor_length(result_tree_cursor_instance, length=2)
    selected_list1 = self.select_asserted_list_of_result_trees(
        result_tree_cursor_instance.location[0],
        length=2,
    )
    self.select_asserted_result_tree(
        selected_list1[0],
        value="B",
        child_values=[],
    )
    self.select_asserted_result_tree(
        selected_list1[1],
        value="B",
        child_values=[],
    )

    selected_list2 = self.select_asserted_list_of_result_trees(
        result_tree_cursor_instance.location[1],
        length=2,
    )
    self.select_asserted_result_tree(
        selected_list2[0],
        value="D",
        child_values=[],
    )
    self.select_asserted_result_tree(
        selected_list2[1],
        value="D",
        child_values=[],
    )

  def test_unique__single_tree__duplicate_children__selects_location(
      self,
      result_tree_cursor_instance: ResultTreeCursor,
  ) -> None:
    mocked_tree = ResultTree(value="A")
    mocked_tree.children = [ResultTree(value="B"), ResultTree(value="B")]
    result_tree_cursor_instance.location.append(mocked_tree)

    result_tree_cursor_instance.unique()

    self.assert_cursor_length(result_tree_cursor_instance, length=1)
    self.select_asserted_result_tree(
        result_tree_cursor_instance.location[0],
        value="A",
        child_values=["B"],
    )

  def test_unique__duplicate_trees__duplicate_children__selects_location(
      self,
      result_tree_cursor_instance: ResultTreeCursor,
  ) -> None:
    mocked_tree1 = ResultTree(value="A")
    mocked_tree1.children = [ResultTree(value="B"), ResultTree(value="B")]
    mocked_tree2 = ResultTree(value="A")
    mocked_tree2.children = [ResultTree(value="C"), ResultTree(value="C")]
    result_tree_cursor_instance.location.append([
        mocked_tree1,
        mocked_tree2,
    ])

    result_tree_cursor_instance.unique()

    self.assert_cursor_length(result_tree_cursor_instance, length=1)
    selected_list = self.select_asserted_list_of_result_trees(
        result_tree_cursor_instance.location[0],
        length=1,
    )
    self.select_asserted_result_tree(
        selected_list[0],
        value="A",
        child_values=["B"],
    )

  def test_unique__unique_trees__duplicate_children__selects_location(
      self,
      result_tree_cursor_instance: ResultTreeCursor,
  ) -> None:
    mocked_tree1 = ResultTree(value="A")
    mocked_tree1.children = [ResultTree(value="B"), ResultTree(value="B")]
    mocked_tree2 = ResultTree(value="C")
    mocked_tree2.children = [ResultTree(value="D"), ResultTree(value="D")]
    result_tree_cursor_instance.location.append([
        mocked_tree1,
        mocked_tree2,
    ])

    result_tree_cursor_instance.unique()

    self.assert_cursor_length(result_tree_cursor_instance, length=1)
    selected_list = self.select_asserted_list_of_result_trees(
        result_tree_cursor_instance.location[0],
        length=2,
    )
    self.select_asserted_result_tree(
        selected_list[0],
        value="A",
        child_values=["B"],
    )
    self.select_asserted_result_tree(
        selected_list[1],
        value="C",
        child_values=["D"],
    )
