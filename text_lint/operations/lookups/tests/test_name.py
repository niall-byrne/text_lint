"""Test the NameLookup class."""

from typing import List
from unittest import mock

import pytest
from text_lint.__helpers__.lookups import (
    assert_is_lookup_failure,
    assert_is_lookup_unknown,
)
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.lookups import LookupFailure, LookupUnknown
from ..bases.lookup_base import LookupBase
from ..name import NameLookup


class TestNameLookup:
  """Test the NameLookup class."""

  def test_initialize__defined__attributes(
      self,
      name_lookup_instance: NameLookup,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "select a named entry from the saved result",
        "lookup_name": mocked_lookup_name,
        "operation": "name",
        "requesting_operation_name": mocked_requesting_operation_name,
        "result_set": mocked_result_set,
    }

    assert_operation_attributes(name_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      name_lookup_instance: NameLookup,
  ) -> None:
    assert_is_translated(name_lookup_instance.hint)
    assert_is_translated(name_lookup_instance.msg_fmt_failure_description)

  def test_initialize__inheritance(
      self,
      name_lookup_instance: NameLookup,
  ) -> None:
    assert_operation_inheritance(
        name_lookup_instance,
        bases=(LookupBase, NameLookup),
    )

  def test_apply__valid_lookup__successful__calls_forest_cursor_flatten(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_trees_grove[0][1].value = name_lookup_instance.lookup_name
    name_lookup_instance.lookup_name = (
        LOOKUP_STATIC_VALUE_MARKER + name_lookup_instance.lookup_name
    )
    mocked_controller.forest.cursor.location = [
        # simulates flattening
        tree for grove in mocked_trees_grove for tree in grove
    ]

    name_lookup_instance.apply(mocked_controller)

    mocked_controller.forest.cursor.flatten.assert_called_once_with()

  def test_apply__valid_lookup__successful__updates_cursor(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_trees_grove[0][1].value = name_lookup_instance.lookup_name
    name_lookup_instance.lookup_name = (
        LOOKUP_STATIC_VALUE_MARKER + name_lookup_instance.lookup_name
    )
    mocked_controller.forest.cursor.location = [
        # simulates flattening
        tree for grove in mocked_trees_grove for tree in grove
    ]

    name_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.cursor.location == [
        mocked_trees_grove[0][1]
    ]

  def test_apply__valid_lookup__successful__updates_lookup_results(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_trees_grove[0][1].value = name_lookup_instance.lookup_name
    name_lookup_instance.lookup_name = (
        LOOKUP_STATIC_VALUE_MARKER + name_lookup_instance.lookup_name
    )
    mocked_controller.forest.cursor.location = [
        # simulates flattening
        tree for grove in mocked_trees_grove for tree in grove
    ]

    name_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.lookup_results == [
        [mocked_trees_grove[0][1].value]
    ]

  def test_apply__valid_lookup__failure__calls_forest_cursor_flatten(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_trees_grove[0][1].value = "non-matching-value"
    name_lookup_instance.lookup_name = (
        LOOKUP_STATIC_VALUE_MARKER + name_lookup_instance.lookup_name
    )
    mocked_controller.forest.cursor.location = [
        # simulates flattening
        tree for grove in mocked_trees_grove for tree in grove
    ]

    with pytest.raises(LookupFailure):
      name_lookup_instance.apply(mocked_controller)

    mocked_controller.forest.cursor.flatten.assert_called_once_with()

  def test_apply__valid_lookup__failure__does_not_update_lookup_results(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_trees_grove[0][1].value = "non-matching-value"
    name_lookup_instance.lookup_name = (
        LOOKUP_STATIC_VALUE_MARKER + name_lookup_instance.lookup_name
    )
    mocked_controller.forest.cursor.location = [
        # simulates flattening
        tree for grove in mocked_trees_grove for tree in grove
    ]

    with pytest.raises(LookupFailure):
      name_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.lookup_results is None

  def test_apply__valid_lookup__failure__raises_lookup_failure(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_trees_grove[0][1].value = "non-matching-value"
    name_lookup_instance.lookup_name = (
        LOOKUP_STATIC_VALUE_MARKER + name_lookup_instance.lookup_name
    )
    mocked_controller.forest.cursor.location = [
        # simulates flattening
        tree for grove in mocked_trees_grove for tree in grove
    ]

    with pytest.raises(LookupFailure) as exc:
      name_lookup_instance.apply(mocked_controller)

    assert_is_lookup_failure(
        exc=exc,
        description_t=(name_lookup_instance.msg_fmt_failure_description,),
        lookup=name_lookup_instance,
    )

  def test_apply__valid_lookup__bad_location__calls_forest_cursor_flatten(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
  ) -> None:
    name_lookup_instance.lookup_name = (
        LOOKUP_STATIC_VALUE_MARKER + name_lookup_instance.lookup_name
    )
    mocked_controller.forest.cursor.location = [None]

    with pytest.raises(LookupFailure):
      name_lookup_instance.apply(mocked_controller)

    mocked_controller.forest.cursor.flatten.assert_called_once_with()

  def test_apply__valid_lookup__bad_location__does_not_update_lookup_results(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
  ) -> None:
    name_lookup_instance.lookup_name = (
        LOOKUP_STATIC_VALUE_MARKER + name_lookup_instance.lookup_name
    )
    mocked_controller.forest.cursor.location = [None]

    with pytest.raises(LookupFailure):
      name_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.lookup_results is None

  def test_apply__valid_lookup__bad_location__raises_lookup_failure(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
  ) -> None:
    name_lookup_instance.lookup_name = (
        LOOKUP_STATIC_VALUE_MARKER + name_lookup_instance.lookup_name
    )
    mocked_controller.forest.cursor.location = [None]

    with pytest.raises(LookupFailure) as exc:
      name_lookup_instance.apply(mocked_controller)

    assert_is_lookup_failure(
        exc=exc,
        description_t=(name_lookup_instance.msg_fmt_failure_description,),
        lookup=name_lookup_instance,
    )

  def test_apply__invalid_lookup__does_not_call_forest_cursor_flatten(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_trees_grove[0][1].value = name_lookup_instance.lookup_name
    name_lookup_instance.lookup_name = name_lookup_instance.lookup_name
    mocked_controller.forest.cursor.location = [
        # simulates flattening
        tree for grove in mocked_trees_grove for tree in grove
    ]

    with pytest.raises(LookupUnknown):
      name_lookup_instance.apply(mocked_controller)

    mocked_controller.forest.cursor.flatten.assert_not_called()

  def test_apply__invalid_lookup__raises_unknown_lookup(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_trees_grove[0][1].value = name_lookup_instance.lookup_name
    name_lookup_instance.lookup_name = name_lookup_instance.lookup_name
    mocked_controller.forest.cursor.location = [
        # simulates flattening
        tree for grove in mocked_trees_grove for tree in grove
    ]

    with pytest.raises(LookupUnknown) as exc:
      name_lookup_instance.apply(mocked_controller)

    assert_is_lookup_unknown(
        exc=exc,
        lookup=name_lookup_instance,
    )

  def test_apply__invalid_lookup__does_not_update_forest_lookup_results(
      self,
      name_lookup_instance: NameLookup,
      mocked_controller: mock.Mock,
      mocked_trees_grove: List[List[mock.Mock]],
  ) -> None:
    mocked_trees_grove[0][1].value = name_lookup_instance.lookup_name
    name_lookup_instance.lookup_name = name_lookup_instance.lookup_name
    mocked_controller.forest.cursor.location = [
        # simulates flattening
        tree for grove in mocked_trees_grove for tree in grove
    ]

    with pytest.raises(LookupUnknown):
      name_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.lookup_results is None
