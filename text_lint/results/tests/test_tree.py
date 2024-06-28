"""Test the ResultTree class."""

from typing import List, Optional

from text_lint.__helpers__.results import assert_result_tree
from ..tree import ResultTree


class TestResultTree:
  """Test the ResultTree class."""

  def test_create__returns_correct_instance(self) -> None:
    instance = ResultTree.create(value="mocked_created_tree")

    assert instance.value == "mocked_created_tree"
    assert isinstance(instance.children, list)
    assert len(instance.children) == 0

  def test_initialize__attributes(
      self,
      result_tree_instance: ResultTree,
  ) -> None:
    assert result_tree_instance.value == "mocked_value"
    assert isinstance(result_tree_instance.children, list)
    assert len(result_tree_instance.children) == 0

  def test_add_matches__no_splits__creates_child_instances(
      self,
      result_tree_instance: ResultTree,
  ) -> None:
    mocked_capture_groups = [
        ("one",),
        ("two",),
        ("three",),
    ]

    for index in range(0, 3):
      result_tree_instance.add_matches(mocked_capture_groups[index], {})

    for index, instance in enumerate(result_tree_instance.children):
      assert isinstance(instance, ResultTree)
      assert instance.value == mocked_capture_groups[index][0]
      assert isinstance(instance.children, list)
      assert len(instance.children) == 0

  def test__eq__same_value__returns_true(self,) -> None:
    tree1 = ResultTree(value="a")
    tree2 = ResultTree(value="a")

    assert tree1 == tree2

  def test__eq__different_value__returns_false(self,) -> None:
    tree1 = ResultTree(value="a")
    tree2 = ResultTree(value="b")

    assert tree1 != tree2

  def test__eq__not_a_tree__returns_false(self,) -> None:
    tree1 = ResultTree(value="a")
    tree2 = "b"

    assert tree1 != tree2

  def test__hash__returns_expected_value(
      self,
      result_tree_instance: ResultTree,
  ) -> None:
    assert hash(result_tree_instance) == hash((result_tree_instance.value,))

  def test_add_matches__no_splits__creates_nested_child_instances(
      self,
      result_tree_instance: ResultTree,
  ) -> None:
    mocked_capture_groups = [
        ("one", "two", "three"),
        ("ALPHA", "BETA", "CHARLIE"),
        ("하나", "둘", "셋"),
    ]

    for index in range(0, 3):
      result_tree_instance.add_matches(mocked_capture_groups[index], {})

    assert len(result_tree_instance.children) == 3
    for index in range(0, 3):
      instance = result_tree_instance.children[index]
      assert isinstance(instance, ResultTree)
      assert len(instance.children) == 1
      assert instance.value == (mocked_capture_groups[index][0])
      instance = result_tree_instance.children[index].children[0]
      assert isinstance(instance, ResultTree)
      assert len(instance.children) == 1
      assert instance.value == (mocked_capture_groups[index][1])
      instance = result_tree_instance.children[index].children[0].children[0]
      assert isinstance(instance, ResultTree)
      assert len(instance.children) == 0
      assert instance.value == (mocked_capture_groups[index][2])

  def test_add_matches__with_splits__creates_child_instances(
      self,
      result_tree_instance: ResultTree,
  ) -> None:
    mocked_capture_groups = [
        ("one two three",),
        ("ALPHA,BETA,CHARLIE",),
        ("하나-둘-셋",),
    ]
    mocked_splits: List[dict[int, Optional[str]]] = [
        {
            1: None
        },
        {
            1: ","
        },
        {
            1: "-"
        },
    ]

    for index in range(0, 3):
      result_tree_instance.add_matches(
          mocked_capture_groups[index],
          mocked_splits[index],
      )

    assert_result_tree(
        result_tree_instance,
        "mocked_value",
        ["one", "two", "three", "ALPHA", "BETA", "CHARLIE", "하나", "둘", "셋"],
    )
    assert_result_tree(result_tree_instance.children[0], "one", [])
    assert_result_tree(result_tree_instance.children[1], "two", [])
    assert_result_tree(result_tree_instance.children[2], "three", [])
    assert_result_tree(result_tree_instance.children[3], "ALPHA", [])
    assert_result_tree(result_tree_instance.children[4], "BETA", [])
    assert_result_tree(result_tree_instance.children[5], "CHARLIE", [])
    assert_result_tree(result_tree_instance.children[6], "하나", [])
    assert_result_tree(result_tree_instance.children[7], "둘", [])
    assert_result_tree(result_tree_instance.children[8], "셋", [])

  def test_add_matches__with_splits__creates_nested_child_instances(
      self,
      result_tree_instance: ResultTree,
  ) -> None:
    mocked_capture_groups = [
        (
            "one two",
            "three",
        ),
        (
            "ALPHA",
            "BETA,CHARLIE",
        ),
        (
            "하나",
            "둘-셋",
        ),
    ]
    mocked_splits: List[dict[int, Optional[str]]] = [
        {
            1: None
        },
        {
            2: ","
        },
        {
            2: "-"
        },
    ]

    for index in range(0, 3):
      result_tree_instance.add_matches(
          mocked_capture_groups[index],
          mocked_splits[index],
      )

    assert_result_tree(
        result_tree_instance,
        "mocked_value",
        ["one", "two", "three", "ALPHA", "하나"],
    )
    assert_result_tree(result_tree_instance.children[0], "one", [])
    assert_result_tree(result_tree_instance.children[1], "two", [])
    assert_result_tree(result_tree_instance.children[2], "three", [])
    assert_result_tree(
        result_tree_instance.children[3], "ALPHA", ["BETA", "CHARLIE"]
    )
    assert_result_tree(result_tree_instance.children[3].children[0], "BETA", [])
    assert_result_tree(
        result_tree_instance.children[3].children[1], "CHARLIE", []
    )
    assert_result_tree(result_tree_instance.children[4], "하나", ["둘", "셋"])
    assert_result_tree(result_tree_instance.children[4].children[0], "둘", [])
    assert_result_tree(result_tree_instance.children[4].children[1], "셋", [])

  def test_representation__no_splits__returns_correct_representation(
      self,
      result_tree_instance: ResultTree,
  ) -> None:
    mocked_capture_groups = [
        ("one", "two", "three"),
        ("ALPHA", "BETA", "CHARLIE"),
        ("하나", "둘", "셋"),
    ]
    for index in range(0, 3):
      result_tree_instance.add_matches(mocked_capture_groups[index], {})

    result = result_tree_instance.representation()

    assert result == {
        'value':
            'mocked_value',
        'children':
            (
                {
                    'value':
                        'one',
                    'children':
                        (
                            {
                                'value':
                                    'two',
                                'children':
                                    ({
                                        'value': 'three',
                                        'children': ()
                                    },)
                            },
                        )
                }, {
                    'value':
                        'ALPHA',
                    'children':
                        (
                            {
                                'value':
                                    'BETA',
                                'children':
                                    ({
                                        'value': 'CHARLIE',
                                        'children': ()
                                    },)
                            },
                        )
                }, {
                    'value':
                        '하나',
                    'children':
                        (
                            {
                                'value': '둘',
                                'children': ({
                                    'value': '셋',
                                    'children': ()
                                },)
                            },
                        )
                }
            )
    }

  def test_representation__with_splits__returns_correct_representation(
      self,
      result_tree_instance: ResultTree,
  ) -> None:
    mocked_capture_groups = [
        (
            "alpha",
            "one two",
            "three",
        ),
        (
            "ALPHA",
            "BETA,CHARLIE",
        ),
        (
            "하나",
            "둘-셋",
        ),
    ]
    mocked_splits: List[dict[int, Optional[str]]] = [
        {
            2: None
        },
        {
            2: ","
        },
        {
            2: "-"
        },
    ]
    for index in range(0, 3):
      result_tree_instance.add_matches(
          mocked_capture_groups[index],
          mocked_splits[index],
      )

    result = result_tree_instance.representation()

    assert result == {
        'value':
            'mocked_value',
        'children':
            (
                {
                    'value':
                        'alpha',
                    'children':
                        (
                            {
                                'value': 'one',
                                'children': ()
                            }, {
                                'value': 'two',
                                'children': ()
                            }
                        )
                }, {
                    'value':
                        'ALPHA',
                    'children':
                        (
                            {
                                'value': 'BETA',
                                'children': ()
                            }, {
                                'value': 'CHARLIE',
                                'children': ()
                            }
                        )
                }, {
                    'value':
                        '하나',
                    'children':
                        (
                            {
                                'value': '둘',
                                'children': ()
                            }, {
                                'value': '셋',
                                'children': ()
                            }
                        )
                }
            )
    }
