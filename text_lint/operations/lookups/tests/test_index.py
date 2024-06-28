"""Test the IndexLookup class."""

from typing import List
from unittest import mock

import pytest
from text_lint.__helpers__.lookups import assert_is_lookup_failure
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.lookups import LookupFailure
from ..bases.lookup_base import LookupBase
from ..index import IndexLookup


class TestIndexLookup:
  """Test the IndexLookup class."""

  def test_initialize__defined__attributes(
      self,
      index_lookup_instance: IndexLookup,
      mocked_lookup_expression: mock.Mock,
      mocked_requesting_operation_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "select a value from a save id by index",
        "is_positional": False,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": "1",
        "operation": "index",
        "requesting_operation_name": mocked_requesting_operation_name,
    }

    assert_operation_attributes(index_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      index_lookup_instance: IndexLookup,
  ) -> None:
    assert_is_translated(index_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      index_lookup_instance: IndexLookup,
  ) -> None:
    assert_operation_inheritance(
        index_lookup_instance,
        bases=(LookupBase, IndexLookup),
    )

  def test_apply__valid_lookup__simple_location__successful__updates_cursor(
      self,
      index_lookup_instance: IndexLookup,
      mocked_state: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_state.cursor.location = [[]]
    mocked_state.cursor.location.append(mocked_trees_grove[0][0])
    mocked_state.results = [["zero"], ["one"]]

    index_lookup_instance.apply(mocked_state)

    assert index_lookup_instance.lookup_name == "1"
    assert mocked_state.cursor.location == [mocked_trees_grove[0][0]]

  def test_apply__valid_lookup__nested_location__successful__updates_cursor(
      self,
      index_lookup_instance: IndexLookup,
      mocked_state: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_state.cursor.location = [[]]
    mocked_state.cursor.location.append(mocked_trees_grove)
    mocked_state.results = [["zero"], ["one"]]

    index_lookup_instance.apply(mocked_state)

    assert index_lookup_instance.lookup_name == "1"
    assert mocked_state.cursor.location == mocked_trees_grove

  def test_apply__valid_lookup__both_indexes_valid__updates_lookup_results(
      self,
      index_lookup_instance: IndexLookup,
      mocked_state: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_state.cursor.location = [[]]
    mocked_state.cursor.location.append(mocked_trees_grove)
    mocked_state.results = [["zero"], ["one"]]

    index_lookup_instance.apply(mocked_state)

    assert index_lookup_instance.lookup_name == "1"
    assert mocked_state.results == ["one"]

  def test_apply__valid_lookup__invalid_location_index__updates_lookup_results(
      self,
      mocked_lookup_expression: mock.Mock,
      mocked_requesting_operation_name: str,
      mocked_state: mock.Mock,
  ) -> None:
    instance = IndexLookup(
        "1",
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )
    mocked_state.cursor.location = [[]]
    mocked_state.results = [["zero"], ["one"]]

    instance.apply(mocked_state)

    assert instance.lookup_name == "1"
    assert mocked_state.results == ["one"]

  def test_apply__valid_lookup__invalid_result_index__raises_exception(
      self,
      mocked_lookup_expression: mock.Mock,
      mocked_requesting_operation_name: str,
      mocked_state: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    instance = IndexLookup(
        "1",
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )
    mocked_state.cursor.location = [[]]
    mocked_state.cursor.location.append(mocked_trees_grove)
    mocked_state.cursor.location.append(mocked_trees_grove)
    mocked_state.results = [["one"]]

    with pytest.raises(LookupFailure) as exc:
      instance.apply(mocked_state)

    assert_is_lookup_failure(
        exc=exc,
        description_t=(
            instance.msg_fmg_invalid_index_description,
            instance.lookup_name,
        ),
        lookup=instance,
    )

  def test_apply__valid_lookup__not_indexed__raises_exception(
      self,
      index_lookup_instance: IndexLookup,
      mocked_state: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_state.cursor.location = [[]]
    mocked_state.cursor.location.append(mocked_trees_grove)
    mocked_state.results = {}

    with pytest.raises(LookupFailure) as exc:
      index_lookup_instance.apply(mocked_state)

    assert_is_lookup_failure(
        exc=exc,
        description_t=(
            index_lookup_instance.msg_fmg_invalid_index_description,
            index_lookup_instance.lookup_name,
        ),
        lookup=index_lookup_instance,
    )
