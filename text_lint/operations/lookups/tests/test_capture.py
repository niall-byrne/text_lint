"""Test the CaptureLookup class."""

from typing import List
from unittest import mock

import pytest
from text_lint.__helpers__.lookups import (
    assert_is_lookup_failure,
    set_lookup_params,
)
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import (
    assert_is_translated,
    assert_is_translated_yaml_example,
)
from text_lint.exceptions.lookups import LookupFailure
from ..bases.lookup_base import AliasLookupParams, LookupBase
from ..capture import YAML_EXAMPLE, YAML_EXAMPLE_COMPONENTS, CaptureLookup


@set_lookup_params([[1]])
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
        "lookup_params": [1],
        "index": 1,
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
    assert_is_translated(capture_lookup_instance.msg_fmg_invalid_capture_group)
    assert_is_translated(capture_lookup_instance.msg_fmg_invalid_parameters)
    assert_is_translated_yaml_example(
        capture_lookup_instance.yaml_example,
        YAML_EXAMPLE_COMPONENTS,
        notes=True,
    )

  def test_initialize__inheritance(
      self,
      capture_lookup_instance: CaptureLookup,
  ) -> None:
    assert_operation_inheritance(
        capture_lookup_instance,
        bases=(LookupBase, CaptureLookup),
    )

  @pytest.mark.parametrize("invalid_params", ([], [1, 2]))
  def test_initialize__invalid_params__raises_exception(
      self,
      capture_lookup_instance: CaptureLookup,
      invalid_params: "AliasLookupParams",
  ) -> None:
    with pytest.raises(LookupFailure) as exc:
      CaptureLookup(
          capture_lookup_instance.lookup_name,
          capture_lookup_instance.lookup_expression,
          invalid_params,
          capture_lookup_instance.requesting_operation_name,
      )

    assert_is_lookup_failure(
        exc=exc,
        description_t=(CaptureLookup.msg_fmg_invalid_parameters,),
        lookup=capture_lookup_instance
    )

  @pytest.mark.parametrize("invalid_params", ([-1], ["a"]))
  def test_initialize__invalid_capture_group__raises_exception(
      self,
      capture_lookup_instance: CaptureLookup,
      invalid_params: "AliasLookupParams",
  ) -> None:
    with pytest.raises(LookupFailure) as exc:
      CaptureLookup(
          capture_lookup_instance.lookup_name,
          capture_lookup_instance.lookup_expression,
          invalid_params,
          capture_lookup_instance.requesting_operation_name,
      )

    assert_is_lookup_failure(
        exc=exc,
        description_t=(
            CaptureLookup.msg_fmg_invalid_capture_group,
            invalid_params[0],
        ),
        lookup=capture_lookup_instance
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
      "fixture_name,expected_result", [
          [
              "mocked_trees_grove",
              ['A', 'A'],
          ],
          ["mocked_trees_woods", ['A', 'B', 'B']],
      ]
  )
  def test_apply__no_traversal__updates_forest_lookup_results(
      self,
      capture_lookup_instance: CaptureLookup,
      mocked_state: mock.Mock,
      fixture_name: str,
      expected_result: List[str],
      request: pytest.FixtureRequest,
  ) -> None:
    mocked_result_trees = request.getfixturevalue(fixture_name)
    mocked_state.cursor.location = mocked_result_trees

    capture_lookup_instance.apply(mocked_state)

    assert mocked_state.results == expected_result

  @pytest.mark.parametrize(
      "fixture_name,expected_result", [
          [
              "mocked_trees_grove",
              ["0", "1", "2", "0", "1", "2"],
          ],
          [
              "mocked_trees_woods",
              ["AA", "BB", "CC", "AA", "EE", "FF", "AA", "EE", "FF"]
          ],
      ]
  )
  def test_apply__with_traversal__updates_forest_lookup_results(
      self,
      capture_lookup_instance: CaptureLookup,
      mocked_state: mock.Mock,
      fixture_name: str,
      expected_result: List[str],
      request: pytest.FixtureRequest,
  ) -> None:
    mocked_result_trees = request.getfixturevalue(fixture_name)
    mocked_state.cursor.location = [
        tree.children for cluster in mocked_result_trees for tree in cluster
    ]

    capture_lookup_instance.apply(mocked_state)

    assert mocked_state.results == expected_result

  def test_apply__invalid_capture_group__updates_forest_lookup_results(
      self,
      capture_lookup_instance: CaptureLookup,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.forest.cursor.location = []

    with pytest.raises(LookupFailure) as exc:
      capture_lookup_instance.apply(mocked_state)

    assert_is_lookup_failure(
        exc=exc,
        description_t=(
            CaptureLookup.msg_fmg_invalid_capture_group,
            capture_lookup_instance.lookup_params[0],
        ),
        lookup=capture_lookup_instance
    )
