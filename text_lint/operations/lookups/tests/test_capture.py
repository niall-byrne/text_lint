"""Test the CaptureLookup class."""

from typing import List
from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from ..bases.lookup_base import LookupBase
from ..capture import YAML_EXAMPLE, CaptureLookup


class TestCaptureLookup:
  """Test the CaptureLookup class."""

  def test_initialize__defined__attributes(
      self,
      capture_lookup_instance: CaptureLookup,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "select the next capture group of the saved result",
        "lookup_name": mocked_lookup_name,
        "operation": "capture",
        "requesting_operation_name": mocked_requesting_operation_name,
        "result_set": mocked_result_set,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(capture_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      capture_lookup_instance: CaptureLookup,
  ) -> None:
    assert_is_translated(capture_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      capture_lookup_instance: CaptureLookup,
  ) -> None:
    assert_operation_inheritance(
        capture_lookup_instance,
        bases=(LookupBase, CaptureLookup),
    )

  def test_apply__calls_forest_cursor_traverse(
      self,
      capture_lookup_instance: CaptureLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_controller.forest.cursor.location = mocked_trees_grove

    capture_lookup_instance.apply(mocked_controller)

    mocked_controller.forest.cursor.traverse.assert_called_once_with()

  @pytest.mark.parametrize(
      "fixture_name", ["mocked_trees_grove", "mocked_trees_woods"]
  )
  def test_apply__updates_forest_lookup_results(
      self,
      capture_lookup_instance: CaptureLookup,
      mocked_controller: mock.Mock,
      fixture_name: str,
      request: pytest.FixtureRequest,
  ) -> None:
    mocked_result_trees = request.getfixturevalue(fixture_name)
    mocked_controller.forest.cursor.location = mocked_result_trees

    capture_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.lookup_results == [
        [child.value
         for child in grove.children]
        for woods in mocked_result_trees
        for grove in woods
    ]
