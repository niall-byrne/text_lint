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
      mocked_lookup_expression: mock.Mock,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      capture_lookup_instance: CaptureLookup,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "select the next capture group of a save id",
        "internal_use_only": False,
        "is_positional": True,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": mocked_lookup_name,
        "lookup_params": [],
        "operation": "capture",
        "requesting_operation_name": mocked_requesting_operation_name,
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

  def test_apply__calls_forest_cursor_increment_depth(
      self,
      capture_lookup_instance: CaptureLookup,
      mocked_state: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_state.cursor.location = mocked_trees_grove

    capture_lookup_instance.apply(mocked_state)

    mocked_state.cursor.increment_depth.assert_called_once_with()

  @pytest.mark.parametrize(
      "fixture_name", ["mocked_trees_grove", "mocked_trees_woods"]
  )
  def test_apply__updates_forest_lookup_results(
      self,
      capture_lookup_instance: CaptureLookup,
      mocked_state: mock.Mock,
      fixture_name: str,
      request: pytest.FixtureRequest,
  ) -> None:
    mocked_result_trees = request.getfixturevalue(fixture_name)
    mocked_state.cursor.location = mocked_result_trees

    capture_lookup_instance.apply(mocked_state)

    assert mocked_state.results == [
        [child.value
         for child in grove.children]
        for woods in mocked_result_trees
        for grove in woods
    ]
