"""Test fixtures for the text_lint results classes."""
# pylint: disable=redefined-outer-name

from typing import List
from unittest import mock

import pytest
from .. import cursor, forest, tree


@pytest.fixture
def mocked_controller() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_existing_tree(
    result_forest_instance: forest.ResultForest,
) -> mock.Mock:
  instance = mock.Mock()
  instance.value = "maple"
  instance.children = [mock.Mock()]
  result_forest_instance.add(instance)
  return instance


@pytest.fixture
def mocked_lookup_operations() -> List[mock.Mock]:
  instances = [mock.Mock(), mock.Mock(), mock.Mock()]
  for index, instance in enumerate(instances):
    instance.results = [index]
  return instances


@pytest.fixture
def mocked_lookup_sequence() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_tree() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def result_tree_cursor_instance() -> cursor.ResultTreeCursor:
  return cursor.ResultTreeCursor()


@pytest.fixture
def result_forest_instance(
    mocked_lookup_operations: mock.Mock,
    mocked_lookup_sequence: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> forest.ResultForest:
  mocked_lookup_sequence.return_value = mocked_lookup_operations
  monkeypatch.setattr(
      forest,
      "LookupsSequencer",
      mocked_lookup_sequence,
  )
  return forest.ResultForest()


@pytest.fixture
def result_tree_instance() -> tree.ResultTree:
  return tree.ResultTree("mocked_value")
