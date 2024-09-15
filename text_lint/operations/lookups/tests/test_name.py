"""Test the NameLookup class."""

from typing import TYPE_CHECKING
from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import (
    assert_is_translated,
    assert_is_translated_yaml_example,
)
from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.utilities.translations import f
from ..bases.lookup_base import LookupBase
from ..name import YAML_EXAMPLE, YAML_EXAMPLE_COMPONENTS, NameLookup

if TYPE_CHECKING:  # no cover
  from text_lint.results.forest import AliasLookupResult


class TestNameLookup:
  """Test the NameLookup class."""

  def test_initialize__defined__attributes(
      self,
      mocked_lookup_expression: mock.Mock,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      name_lookup_instance: NameLookup,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "select a static value from a save id",
        "internal_use_only": False,
        "is_positional": False,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": mocked_lookup_name,
        "lookup_params": [],
        "operation": "name",
        "requesting_operation_name": mocked_requesting_operation_name,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(name_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      name_lookup_instance: NameLookup,
  ) -> None:
    assert_is_translated(name_lookup_instance.hint)
    assert_is_translated(name_lookup_instance.msg_fmt_failure_description)
    assert_is_translated_yaml_example(
        name_lookup_instance.yaml_example,
        YAML_EXAMPLE_COMPONENTS,
        notes=True,
    )

  def test_initialize__inheritance(
      self,
      name_lookup_instance: NameLookup,
  ) -> None:
    assert_operation_inheritance(
        name_lookup_instance,
        bases=(LookupBase, NameLookup),
    )

  @pytest.mark.parametrize(
      "scenario_fixture", [
          "scenario__name_lookup__matching_str_tree",
          "scenario__name_lookup__non_matching_tree",
      ]
  )
  def test_apply__vary_tree__matching_result__calls_cursor_flatten(
      self,
      name_lookup_instance: NameLookup,
      scenario_fixture: str,
      request: pytest.FixtureRequest,
  ) -> None:
    scenario = request.getfixturevalue(scenario_fixture)
    scenario.mocked_state.results = [scenario.mocked_lookup_name]

    name_lookup_instance.apply(scenario.mocked_state)

    scenario.mocked_state.cursor.flatten.assert_called_once_with()

  @pytest.mark.parametrize(
      "scenario_fixture", [
          "scenario__name_lookup__matching_str_tree",
          "scenario__name_lookup__matching_list_tree",
      ]
  )
  def test_apply__vary_matching__matching_result__updates_cursor_location(
      self,
      name_lookup_instance: NameLookup,
      scenario_fixture: str,
      request: pytest.FixtureRequest,
  ) -> None:
    scenario = request.getfixturevalue(scenario_fixture)
    scenario.mocked_state.results = [scenario.mocked_lookup_name]

    name_lookup_instance.apply(scenario.mocked_state)

    assert scenario.mocked_state.cursor.location == [
        scenario.mocked_trees_grove[0][1]
    ]

  @pytest.mark.usefixtures("scenario__name_lookup__non_matching_tree")
  def test_apply__non_matching_tree__matching_result__no_cursor_update(
      self,
      name_lookup_instance: NameLookup,
      mocked_state: mock.Mock,
      mocked_lookup_name: str,
  ) -> None:
    original_position = mocked_state.cursor.location
    mocked_state.results = [mocked_lookup_name]

    name_lookup_instance.apply(mocked_state)

    assert mocked_state.cursor.location == original_position

  @pytest.mark.parametrize(
      "mocked_lookup_result,expected_results", [
          [
              "mocked_lookup_name",
              "mocked_lookup_name",
          ],
          [
              ["mocked_lookup_name"],
              ["mocked_lookup_name"],
          ],
          [
              ("mocked_lookup_name", "other value"),
              ("mocked_lookup_name", "other value"),
          ],
          [
              [["mocked_lookup_name"], ["other value"]],
              [["mocked_lookup_name"]],
          ],
          [
              {
                  "mocked_lookup_name": "matching dict"
              },
              {
                  "mocked_lookup_name": "matching dict"
              },
          ],
          [
              {
                  "matching nested dict": {
                      "mocked_lookup_name": "nested dict"
                  }
              },
              {
                  "mocked_lookup_name": "nested dict"
              },
          ],
          [
              [
                  {
                      "mocked_lookup_name": "matching dict in list"
                  },
                  {
                      "non matching key": "non matching dict in list"
                  },
              ],
              [
                  {
                      "mocked_lookup_name": "matching dict in list"
                  },
              ],
          ],
      ]
  )
  @pytest.mark.parametrize(
      "scenario_fixture", [
          "scenario__name_lookup__matching_str_tree",
          "scenario__name_lookup__non_matching_tree",
      ]
  )
  def test_apply__vary_tree__vary_matching_result__updates_results(
      self,
      name_lookup_instance: NameLookup,
      mocked_lookup_result: "AliasLookupResult",
      expected_results: "AliasLookupResult",
      scenario_fixture: str,
      request: pytest.FixtureRequest,
  ) -> None:
    scenario = request.getfixturevalue(scenario_fixture)
    scenario.mocked_state.results = mocked_lookup_result
    name_lookup_instance.lookup_name = (
        LOOKUP_STATIC_VALUE_MARKER + "mocked_lookup_name"
    )

    name_lookup_instance.apply(scenario.mocked_state)

    assert scenario.mocked_state.results == expected_results

  @pytest.mark.parametrize(
      "scenario_fixture", [
          "scenario__name_lookup__matching_str_tree",
          "scenario__name_lookup__non_matching_tree",
      ]
  )
  def test_apply__matching_tree__non_matching_str__does_not_update_results(
      self,
      name_lookup_instance: NameLookup,
      scenario_fixture: str,
      request: pytest.FixtureRequest,
  ) -> None:
    scenario = request.getfixturevalue(scenario_fixture)
    scenario.mocked_state.results = None

    name_lookup_instance.apply(scenario.mocked_state)

    assert scenario.mocked_state.results is None

  @pytest.mark.parametrize(
      "non_matching_results", [
          "non matching_string",
          ["non", "matching", "list"],
          {
              "non": "matching dict"
          },
      ]
  )
  @pytest.mark.parametrize(
      "scenario_fixture", [
          "scenario__name_lookup__matching_str_tree",
          "scenario__name_lookup__non_matching_tree",
      ]
  )
  def test_apply__vary_tree__vary_non_matching__raises_lookup_failure(
      self,
      name_lookup_instance: NameLookup,
      non_matching_results: "AliasLookupResult",
      scenario_fixture: str,
      request: pytest.FixtureRequest,
  ) -> None:
    scenario = request.getfixturevalue(scenario_fixture)
    scenario.mocked_state.results = non_matching_results

    name_lookup_instance.apply(scenario.mocked_state)

    scenario.mocked_state.fail.assert_called_once_with(
        translated_description=f(
            name_lookup_instance.msg_fmt_failure_description, nl=1
        ),
        operation=name_lookup_instance,
    )
