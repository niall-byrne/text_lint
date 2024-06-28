"""Test the NoopLookup class."""

from typing import List
from unittest import mock

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from ..bases.lookup_base import LookupBase
from ..noop import NoopLookup


class TestNoopLookup:
  """Test the NoopLookup class."""

  def test_initialize__defined__attributes(
      self,
      noop_lookup_instance: NoopLookup,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "a simple no-operation",
        "lookup_name": mocked_lookup_name,
        "operation": "noop",
        "requesting_operation_name": mocked_requesting_operation_name,
        "result_set": mocked_result_set,
    }

    assert_operation_attributes(noop_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      noop_lookup_instance: NoopLookup,
  ) -> None:
    assert_is_translated(noop_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      noop_lookup_instance: NoopLookup,
  ) -> None:
    assert_operation_inheritance(
        noop_lookup_instance,
        bases=(LookupBase, NoopLookup),
    )

  def test_apply__does_not_modify_forest_cursor(
      self,
      noop_lookup_instance: NoopLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_controller.forest.cursor.location = mocked_trees_grove

    noop_lookup_instance.apply(mocked_controller)

    mocked_controller.forest.cursor.traverse.assert_not_called()
    mocked_controller.forest.cursor.flatten.assert_not_called()

  def test_apply__does_not_modify_forest_lookup_results(
      self,
      noop_lookup_instance: NoopLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_controller.forest.cursor.location = mocked_trees_grove

    noop_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.lookup_results is None
