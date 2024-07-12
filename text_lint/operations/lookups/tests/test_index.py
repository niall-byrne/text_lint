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
from ..index import YAML_EXAMPLE, IndexLookup


class TestIndexLookup:
  """Test the IndexLookup class."""

  def test_initialize__defined__attributes(
      self,
      index_lookup_instance: IndexLookup,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "select an entry from the saved results by index",
        "internal_use_only": False,
        "lookup_name": "1",
        "operation": "index",
        "requesting_operation_name": mocked_requesting_operation_name,
        "result_set": mocked_result_set,
        "yaml_example": YAML_EXAMPLE,
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
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_controller.forest.cursor.location = [[]]
    mocked_controller.forest.cursor.location.append(mocked_trees_grove[0][0])
    mocked_controller.forest.lookup_results = [["one"], ["two"]]

    index_lookup_instance.apply(mocked_controller)

    assert index_lookup_instance.lookup_name == "1"
    assert mocked_controller.forest.cursor.location == [
        mocked_trees_grove[0][0]
    ]

  def test_apply__valid_lookup__nested_location__successful__updates_cursor(
      self,
      index_lookup_instance: IndexLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_controller.forest.cursor.location = [[]]
    mocked_controller.forest.cursor.location.append(mocked_trees_grove)
    mocked_controller.forest.lookup_results = [["one"], ["two"]]

    index_lookup_instance.apply(mocked_controller)

    assert index_lookup_instance.lookup_name == "1"
    assert mocked_controller.forest.cursor.location == mocked_trees_grove

  def test_apply__valid_lookup__successful__updates_forest_lookup_results(
      self,
      index_lookup_instance: IndexLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_controller.forest.cursor.location = [[]]
    mocked_controller.forest.cursor.location.append(mocked_trees_grove)
    mocked_controller.forest.lookup_results = [["one"], ["two"]]

    index_lookup_instance.apply(mocked_controller)

    assert index_lookup_instance.lookup_name == "1"
    assert mocked_controller.forest.lookup_results == ["two"]

  def test_apply__valid_lookup__out_of_range__raises_exception(
      self,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    instance = IndexLookup(
        "2",
        mocked_result_set,
        mocked_requesting_operation_name,
    )
    mocked_controller.forest.cursor.location = [[]]
    mocked_controller.forest.cursor.location.append(mocked_trees_grove)
    mocked_controller.forest.lookup_results = [["one"], ["two"]]

    with pytest.raises(LookupFailure) as exc:
      instance.apply(mocked_controller)

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
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_controller.forest.cursor.location = [[]]
    mocked_controller.forest.cursor.location.append(mocked_trees_grove)
    mocked_controller.forest.lookup_results = {}

    with pytest.raises(LookupFailure) as exc:
      index_lookup_instance.apply(mocked_controller)

    assert_is_lookup_failure(
        exc=exc,
        description_t=(
            index_lookup_instance.msg_fmg_invalid_index_description,
            index_lookup_instance.lookup_name,
        ),
        lookup=index_lookup_instance,
    )
