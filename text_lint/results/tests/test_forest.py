"""Test the ResultForest class."""

from typing import List
from unittest import mock

import pytest
from text_lint.__helpers__.results import assert_is_result_does_not_exist
from text_lint.__helpers__.translations import assert_is_translated
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
    assert isinstance(result_forest_instance.trees, dict)
    assert len(result_forest_instance.trees) == 0
    assert isinstance(result_forest_instance.lookup_results, list)
    assert len(result_forest_instance.lookup_results) == 0
    assert isinstance(result_forest_instance.cursor, ResultTreeCursor)

  def test_initialize__translations(
      self,
      result_forest_instance: ResultForest,
  ) -> None:
    assert_is_translated(result_forest_instance.msg_fmt_does_not_exist_hint)

  def test_add__no_tree__no_op(
      self,
      result_forest_instance: ResultForest,
  ) -> None:

    result_forest_instance.add(None)

    assert len(result_forest_instance.trees) == 0

  def test_add__no_existing__appends_new_tree(
      self,
      result_forest_instance: ResultForest,
      mocked_tree: mock.Mock,
  ) -> None:
    mocked_tree.value = "spruce"

    result_forest_instance.add(mocked_tree)

    assert len(result_forest_instance.trees) == 1
    assert result_forest_instance.trees["spruce"] == mocked_tree

  def test_add__existing__merges_tree_children(
      self,
      result_forest_instance: ResultForest,
      mocked_existing_tree: mock.Mock,
      mocked_tree: mock.Mock,
      mocked_woods: mock.Mock,
  ) -> None:
    mocked_tree.value = mocked_existing_tree.value
    mocked_tree.children = mocked_woods
    existing_child_tree = mocked_existing_tree.children[0]

    result_forest_instance.add(mocked_tree)

    assert len(result_forest_instance.trees) == 1
    assert result_forest_instance.\
        trees[mocked_tree.value] == mocked_existing_tree
    assert result_forest_instance.\
        trees[mocked_tree.value].children == (
            [existing_child_tree] + mocked_woods
        )

  def test_lookup__uses_cloned_cursor(
      self,
      result_forest_instance: ResultForest,
      mocked_controller: mock.Mock,
      mocked_existing_tree: mock.Mock,
  ) -> None:
    mocked_cursor = mock.Mock()
    result_forest_instance.cursor = mocked_cursor
    mocked_requested_result = mock.Mock()
    mocked_requested_result.source = mocked_existing_tree.value
    mocked_requesting_operation = "mocked_requesting_operation"

    result_forest_instance.lookup(
        mocked_controller,
        mocked_requested_result,
        mocked_requesting_operation,
    )

    mocked_cursor.clone.assert_called_once_with()
    assert result_forest_instance.cursor == mocked_cursor.clone.return_value

  def test_lookup__creates_lookup_sequence(
      self,
      result_forest_instance: ResultForest,
      mocked_controller: mock.Mock,
      mocked_existing_tree: mock.Mock,
      mocked_lookup_sequence: mock.Mock,
  ) -> None:
    mocked_requested_result = mock.Mock()
    mocked_requested_result.source = mocked_existing_tree.value
    mocked_requesting_operation = "mocked_requesting_operation"

    result_forest_instance.lookup(
        mocked_controller,
        mocked_requested_result,
        mocked_requesting_operation,
    )

    mocked_lookup_sequence.assert_called_once_with(
        mocked_requested_result,
        mocked_requesting_operation,
    )

  def test_lookup__existing__calls_all_lookup_operations(
      self,
      result_forest_instance: ResultForest,
      mocked_controller: mock.Mock,
      mocked_existing_tree: mock.Mock,
      mocked_lookup_operations: List[mock.Mock],
  ) -> None:
    mocked_requested_result = mock.Mock()
    mocked_requested_result.source = mocked_existing_tree.value
    mocked_requesting_operation = "mocked_requesting_operation"

    result_forest_instance.lookup(
        mocked_controller,
        mocked_requested_result,
        mocked_requesting_operation,
    )

    for mock_operation in mocked_lookup_operations:
      mock_operation.apply.assert_called_once_with(mocked_controller)

  def test_lookup__existing__returns_correct_results(
      self,
      result_forest_instance: ResultForest,
      mocked_controller: mock.Mock,
      mocked_existing_tree: mock.Mock,
  ) -> None:
    mocked_requested_result = mock.Mock()
    mocked_requested_result.source = mocked_existing_tree.value
    mocked_requesting_operation = "mocked_requesting_operation"

    lookup_results = result_forest_instance.lookup(
        mocked_controller,
        mocked_requested_result,
        mocked_requesting_operation,
    )

    assert lookup_results == [[mocked_requested_result.source]]

  def test_lookup__no_existing__raises_does_not_exist(
      self,
      result_forest_instance: ResultForest,
      mocked_controller: mock.Mock,
  ) -> None:
    mocked_requested_result = mock.Mock()
    mocked_requested_result.source = "non_existing_source"
    mocked_requesting_operation = "mocked_requesting_operation"

    with pytest.raises(ResultDoesNotExist) as exc:
      result_forest_instance.lookup(
          mocked_controller,
          mocked_requested_result,
          mocked_requesting_operation,
      )

    assert_is_result_does_not_exist(
        exc=exc,
        result_set=mocked_requested_result,
        requesting_operation_name=mocked_requesting_operation,
        hint=result_forest_instance.msg_fmt_does_not_exist_hint,
    )

  def test_lookup__static_value__returns_correct_results(
      self,
      result_forest_instance: ResultForest,
      mocked_controller: mock.Mock,
  ) -> None:
    mocked_requested_result = mock.Mock()
    mocked_requested_result.source = LOOKUP_STATIC_VALUE_MARKER + "static value"
    mocked_requesting_operation = "mocked_requesting_operation"

    lookup_results = result_forest_instance.lookup(
        mocked_controller,
        mocked_requested_result,
        mocked_requesting_operation,
    )

    assert lookup_results == mocked_requested_result.source[1:]
