"""Test the ResultTree class."""

from typing import Dict, List, Optional

import pytest
from text_lint.__helpers__.results import assert_result_tree
from text_lint.exceptions.results import SplitGroupNotFound
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
    mocked_splits: List[Dict[int, Optional[str]]] = [
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
        result_tree_instance.children[0],
        ["one", "two", "three"],
        [],
    )
    assert_result_tree(
        result_tree_instance.children[1],
        ["ALPHA", "BETA", "CHARLIE"],
        [],
    )
    assert_result_tree(
        result_tree_instance.children[2],
        ["하나", "둘", "셋"],
        [],
    )

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
    mocked_splits: List[Dict[int, Optional[str]]] = [
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
        result_tree_instance.children[0],
        ["one", "two"],
        ["three"],
    )
    assert_result_tree(
        result_tree_instance.children[1],
        "ALPHA",
        [['BETA', 'CHARLIE']],
    )
    assert_result_tree(
        result_tree_instance.children[2],
        "하나",
        [['둘', '셋']],
    )

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
        'capture':
            [
                {
                    'value':
                        'one',
                    'capture':
                        [
                            {
                                'value': 'two',
                                'capture': [{
                                    'value': 'three',
                                    'capture': []
                                }]
                            }
                        ]
                }, {
                    'value':
                        'ALPHA',
                    'capture':
                        [
                            {
                                'value': 'BETA',
                                'capture': [
                                    {
                                        'value': 'CHARLIE',
                                        'capture': []
                                    }
                                ]
                            }
                        ]
                }, {
                    'value':
                        '하나',
                    'capture':
                        [
                            {
                                'value': '둘',
                                'capture': [{
                                    'value': '셋',
                                    'capture': []
                                }]
                            }
                        ]
                }
            ]
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
    mocked_splits: List[Dict[int, Optional[str]]] = [
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
        'capture':
            [
                {
                    'value':
                        'alpha',
                    'capture':
                        [
                            {
                                'value': ['one', 'two'],
                                'capture': [{
                                    'value': 'three',
                                    'capture': []
                                }]
                            }
                        ]
                }, {
                    'value': 'ALPHA',
                    'capture': [{
                        'value': ['BETA', 'CHARLIE'],
                        'capture': []
                    }]
                }, {
                    'value': '하나',
                    'capture': [{
                        'value': ['둘', '셋'],
                        'capture': []
                    }]
                }
            ]
    }

  def test_add_matches__invalid_splits__raises_exception(
      self,
      result_tree_instance: ResultTree,
  ) -> None:
    mocked_capture_group = ("one", "two", "three")
    mocked_splits: Dict[int, Optional[str]] = {4: None}

    with pytest.raises(SplitGroupNotFound) as exc:
      result_tree_instance.add_matches(
          mocked_capture_group,
          mocked_splits,
      )

    assert exc.value.group == 4
