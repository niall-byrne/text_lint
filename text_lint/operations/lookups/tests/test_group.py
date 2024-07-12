"""Test the GroupLookup class."""

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
from ..group import YAML_EXAMPLE, GroupLookup


class TestGroupLookup:
  """Test the GroupLookup class."""

  def test_initialize__defined__attributes(
      self,
      group_lookup_instance: GroupLookup,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "group the currently selected values of the saved result",
        "internal_use_only": False,
        "lookup_name": mocked_lookup_name,
        "operation": "group",
        "requesting_operation_name": mocked_requesting_operation_name,
        "result_set": mocked_result_set,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(group_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      group_lookup_instance: GroupLookup,
  ) -> None:
    assert_is_translated(group_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      group_lookup_instance: GroupLookup,
  ) -> None:
    assert_operation_inheritance(
        group_lookup_instance,
        bases=(LookupBase, GroupLookup),
    )

  def test_apply__calls_forest_cursor_flatten(
      self,
      group_lookup_instance: GroupLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[mock.Mock],
  ) -> None:
    mocked_controller.forest.lookup_results = [mocked_trees_grove]

    group_lookup_instance.apply(mocked_controller)

    mocked_controller.forest.cursor.flatten.assert_called_once_with()

  @pytest.mark.parametrize(
      "fixture_name", ["mocked_trees_grove", "mocked_trees_woods"]
  )
  def test_apply__updates_forest_lookup_results(
      self,
      group_lookup_instance: GroupLookup,
      mocked_controller: mock.Mock,
      fixture_name: str,
      request: pytest.FixtureRequest,
  ) -> None:
    mocked_result_trees = request.getfixturevalue(fixture_name)
    mocked_controller.forest.lookup_results = [mocked_result_trees]

    group_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.lookup_results == [
        list(mocked_result_trees)
    ]
