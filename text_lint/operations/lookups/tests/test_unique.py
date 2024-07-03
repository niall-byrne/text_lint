"""Test the UniqueFilterLookup class."""

from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.operations.lookups.bases.lookup_base import LookupBase
from .. import unique
from ..unique import YAML_EXAMPLE, UniqueFilterLookup


class TestUniqueFilterLookup:
  """Test the UniqueFilterLookup class."""

  def test_initialize__defined__attributes(
      self,
      unique_lookup_instance: UniqueFilterLookup,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "filter unique values from the saved result",
        "lookup_name": mocked_lookup_name,
        "operation": "unique",
        "requesting_operation_name": mocked_requesting_operation_name,
        "result_set": mocked_result_set,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(unique_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      unique_lookup_instance: UniqueFilterLookup,
  ) -> None:
    assert_is_translated(unique_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      unique_lookup_instance: UniqueFilterLookup,
  ) -> None:
    assert_operation_inheritance(
        unique_lookup_instance,
        bases=(
            LookupBase,
            UniqueFilterLookup,
        ),
    )

  def test_apply__calls_cursor_unique_method(
      self,
      unique_lookup_instance: UniqueFilterLookup,
      mocked_controller: mock.Mock,
      mocked_trees_woods: mock.Mock,
  ) -> None:
    mocked_controller.forest.lookup_results = "mock_results"
    mocked_controller.forest.cursor.location = mocked_trees_woods

    unique_lookup_instance.apply(mocked_controller)

    mocked_controller.forest.cursor.unique.assert_called_once_with()

  def test_apply__delegates_result_changes_to_unique_lookup(
      self,
      unique_lookup_instance: UniqueFilterLookup,
      mocked_controller: mock.Mock,
      mocked_trees_woods: mock.Mock,
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    mocked_unique_lookup = mock.Mock()
    mocked_controller.forest.cursor.location = mocked_trees_woods
    monkeypatch.setattr(
        unique,
        "UniqueLookup",
        mocked_unique_lookup,
    )

    unique_lookup_instance.apply(mocked_controller)

    mocked_unique_lookup.assert_called_once_with(
        unique_lookup_instance.lookup_name,
        unique_lookup_instance.result_set,
        unique_lookup_instance.requesting_operation_name,
    )
    mocked_unique_lookup.return_value.apply.assert_called_once_with(
        mocked_controller
    )
