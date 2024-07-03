"""Test the GroupLookup class."""

from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from ..bases.lookup_base import LookupBase
from ..to_group import YAML_EXAMPLE, GroupLookup


class TestGroupLookup:
  """Test the GroupLookup class."""

  def test_initialize__defined__attributes(
      self,
      mocked_lookup_expression: mock.Mock,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      to_group_lookup_instance: GroupLookup,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "group the values of a save id",
        "is_positional": False,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": mocked_lookup_name,
        "operation": LOOKUP_TRANSFORMATION_PREFIX + "group",
        "requesting_operation_name": mocked_requesting_operation_name,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(to_group_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      to_group_lookup_instance: GroupLookup,
  ) -> None:
    assert_is_translated(to_group_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      to_group_lookup_instance: GroupLookup,
  ) -> None:
    assert_operation_inheritance(
        to_group_lookup_instance,
        bases=(LookupBase, GroupLookup),
    )

  @pytest.mark.parametrize(
      "fixture_name", ["mocked_trees_grove", "mocked_trees_woods"]
  )
  def test_apply__updates_forest_lookup_results(
      self,
      to_group_lookup_instance: GroupLookup,
      mocked_state: mock.Mock,
      fixture_name: str,
      request: pytest.FixtureRequest,
  ) -> None:
    mocked_result_trees = request.getfixturevalue(fixture_name)
    mocked_state.results = [mocked_result_trees]

    to_group_lookup_instance.apply(mocked_state)

    assert mocked_state.results == list(mocked_result_trees)
