"""Test the ResultForest class."""

from typing import List, Union
from unittest import mock

import pytest
from text_lint.__helpers__.results import assert_is_result_does_not_exist
from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.results import ResultDoesNotExist
from ..cursor import ResultTreeCursor
from ..forest import ResultForest


class TestResultForest:
  """Test the ResultForest class."""

  def test_initialize__attributes(
      self,
      result_forest_instance: ResultForest,
  ) -> None:
    assert len(result_forest_instance) == 0
    assert isinstance(result_forest_instance.lookup_results, list)
    assert len(result_forest_instance.lookup_results) == 0
    assert isinstance(result_forest_instance.cursor, ResultTreeCursor)

  def test_len__no_tree__returns_zero(
      self,
      result_forest_instance: ResultForest,
  ) -> None:

    # pylint: disable=protected-access
    result_forest_instance._trees = {}

    assert len(result_forest_instance) == 0

  def test_len__three_trees__returns_three(
      self,
      result_forest_instance: ResultForest,
  ) -> None:

    # pylint: disable=protected-access
    result_forest_instance._trees = {
        "one": mock.Mock(),
        "two": mock.Mock(),
        "three": mock.Mock(),
    }

    assert len(result_forest_instance) == 3

  def test_add__no_tree__no_op(
      self,
      result_forest_instance: ResultForest,
  ) -> None:

    result_forest_instance.add(None)

    assert len(result_forest_instance) == 0

  @pytest.mark.parametrize("new_tree_value", ["spruce", ["maple", "pine"]])
  def test_add__vary_value__no_existing__appends_new_tree(
      self,
      result_forest_instance: ResultForest,
      mocked_tree: mock.Mock,
      new_tree_value: Union[str, List[str]],
  ) -> None:
    mocked_tree.value = new_tree_value

    result_forest_instance.add(mocked_tree)

    assert len(result_forest_instance) == 1
    assert result_forest_instance.get(new_tree_value) == mocked_tree

  @pytest.mark.parametrize("new_tree_value", ["spruce", ["maple", "pine"]])
  def test_add__vary_name__merges_tree_children(
      self,
      result_forest_instance: ResultForest,
      mocked_tree: mock.Mock,
      new_tree_value: Union[str, List[str]],
  ) -> None:
    mocked_existing_tree = mock.Mock()
    mocked_existing_child_tree = mock.Mock()
    mocked_existing_tree.value = new_tree_value
    mocked_existing_tree.children = [mocked_existing_child_tree]
    mocked_tree.value = new_tree_value
    mocked_tree.children = [mock.Mock(), mock.Mock()]

    result_forest_instance.add(mocked_existing_tree)
    result_forest_instance.add(mocked_tree)

    assert len(result_forest_instance) == 1
    assert result_forest_instance.get(new_tree_value) == \
        mocked_existing_tree
    assert result_forest_instance.get(new_tree_value).children == \
        [mocked_existing_child_tree] + mocked_tree.children

  def test_lookup_expression__valid_source__valid_lookup__uses_cloned_cursor(
      self,
      result_forest_instance: ResultForest,
      mocked_linter: mock.Mock,
      mocked_existing_tree: mock.Mock,
  ) -> None:
    mocked_cursor = mock.Mock()
    result_forest_instance.cursor = mocked_cursor
    mocked_lookup_expression = mock.Mock()
    mocked_lookup_expression.source = mocked_existing_tree.value

    result_forest_instance.lookup_expression(
        mocked_linter,
        mocked_lookup_expression,
    )

    mocked_cursor.clone.assert_called_once_with()
    assert result_forest_instance.cursor == mocked_cursor.clone.return_value

  def test_lookup_expression__valid_source__creates_lookup_sequence(
      self,
      result_forest_instance: ResultForest,
      mocked_linter: mock.Mock,
      mocked_existing_tree: mock.Mock,
      mocked_lookup_sequencer: mock.Mock,
  ) -> None:
    mocked_lookup_expression = mock.Mock()
    mocked_lookup_expression.source = mocked_existing_tree.value

    result_forest_instance.lookup_expression(
        mocked_linter,
        mocked_lookup_expression,
    )

    mocked_lookup_sequencer.assert_called_once_with(
        mocked_lookup_expression,
        mocked_linter.validators.last.name,
    )

  def test_lookup_expression__valid_source__applies_all_operations(
      self,
      result_forest_instance: ResultForest,
      mocked_linter: mock.Mock,
      mocked_existing_tree: mock.Mock,
      mocked_lookup_operations: List[mock.Mock],
  ) -> None:
    mocked_lookup_expression = mock.Mock()
    mocked_lookup_expression.source = mocked_existing_tree.value

    result_forest_instance.lookup_expression(
        mocked_linter,
        mocked_lookup_expression,
    )

    for mock_operation in mocked_lookup_operations:
      mock_operation.apply.assert_called_once_with(
          mocked_linter.states.lookup.return_value
      )

  def test_lookup_expression__valid_source__returns_correct_results(
      self,
      result_forest_instance: ResultForest,
      mocked_linter: mock.Mock,
      mocked_existing_tree: mock.Mock,
  ) -> None:
    mocked_lookup_expression = mock.Mock()
    mocked_lookup_expression.source = mocked_existing_tree.value

    lookup_results = result_forest_instance.lookup_expression(
        mocked_linter,
        mocked_lookup_expression,
    )

    assert lookup_results == [[mocked_lookup_expression.source]]

  def test_lookup_expression__invalid_source__raises_does_not_exist(
      self,
      result_forest_instance: ResultForest,
      mocked_linter: mock.Mock,
  ) -> None:
    mocked_lookup_expression = mock.Mock()
    mocked_lookup_expression.source = "non_existing_source"

    with pytest.raises(ResultDoesNotExist) as exc:
      result_forest_instance.lookup_expression(
          mocked_linter,
          mocked_lookup_expression,
      )

    assert_is_result_does_not_exist(
        exc=exc,
        lookup_expression=mocked_lookup_expression,
        requesting_operation_name=mocked_linter.validators.last.name,
        hint=ResultDoesNotExist.msg_fmt_does_not_exist_hint,
    )

  def test_lookup_expression__valid_static_value__returns_correct_results(
      self,
      result_forest_instance: ResultForest,
      mocked_linter: mock.Mock,
  ) -> None:
    mocked_lookup_expression = mock.Mock()
    mocked_lookup_expression.source = (
        LOOKUP_STATIC_VALUE_MARKER + "static value"
    )

    lookup_results = result_forest_instance.lookup_expression(
        mocked_linter,
        mocked_lookup_expression,
    )

    assert lookup_results == mocked_lookup_expression.source[1:]
