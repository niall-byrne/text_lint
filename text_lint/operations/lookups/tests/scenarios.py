"""Test scenarios for the lookup operator tests."""
# pylint: disable=redefined-outer-name

from typing import List, NamedTuple
from unittest import mock

import pytest
from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.operations.lookups.name import NameLookup
from text_lint.results.tree import ResultTree

__all__ = (
    "ScenarioNameLookup",
    "scenario__name_lookup__scenario_base",
    "scenario__name_lookup__matching_str_tree",
    "scenario__name_lookup__matching_list_tree",
    "scenario__name_lookup__matching_list_tree",
    "scenario__name_lookup__non_matching_tree",
)


class ScenarioNameLookup(NamedTuple):
  name_lookup_instance: NameLookup
  mocked_lookup_name: str
  mocked_controller: mock.Mock
  mocked_trees_grove: List[List[mock.Mock]]


@pytest.fixture
def scenario__name_lookup__scenario_base(
    name_lookup_instance: NameLookup,
    mocked_controller: mock.Mock,
    mocked_lookup_name: str,
    mocked_trees_grove: List[List[mock.Mock]],
) -> ScenarioNameLookup:
  name_lookup_instance.lookup_name = (
      LOOKUP_STATIC_VALUE_MARKER + mocked_lookup_name
  )
  mocked_controller.forest.cursor.location = [
      # simulates flattening
      tree for grove in mocked_trees_grove for tree in grove
  ]

  return ScenarioNameLookup(
      name_lookup_instance=name_lookup_instance,
      mocked_lookup_name=mocked_lookup_name,
      mocked_controller=mocked_controller,
      mocked_trees_grove=mocked_trees_grove,
  )


@pytest.fixture
def scenario__name_lookup__matching_str_tree(
    scenario__name_lookup__scenario_base: ScenarioNameLookup,
) -> ScenarioNameLookup:
  scenario__name_lookup__scenario_base.mocked_trees_grove[0][1].value = (
      scenario__name_lookup__scenario_base.mocked_lookup_name
  )
  return scenario__name_lookup__scenario_base


@pytest.fixture
def scenario__name_lookup__matching_list_tree(
    scenario__name_lookup__scenario_base: ScenarioNameLookup,
) -> ScenarioNameLookup:
  scenario__name_lookup__scenario_base.mocked_trees_grove[0][1].value = (
      [
          scenario__name_lookup__scenario_base.mocked_lookup_name,
          "other value",
      ]
  )
  return scenario__name_lookup__scenario_base


@pytest.fixture
def scenario__name_lookup__non_matching_tree(
    scenario__name_lookup__scenario_base: ScenarioNameLookup,
) -> ScenarioNameLookup:
  mock_tree = mock.Mock(spec=ResultTree)
  mock_tree.value = ["1", "2", "3"]
  scenario__name_lookup__scenario_base.\
      mocked_controller.forest.cursor.location = [mock_tree]
  return scenario__name_lookup__scenario_base
