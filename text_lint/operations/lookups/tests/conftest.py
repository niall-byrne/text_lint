"""Test fixtures for the text_lint lookup operations."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, Callable, Dict, List
from unittest import mock

import pytest
from text_lint.operations.lookups.bases.lookup_base import LookupBase
from text_lint.results.tree import ResultTree
from .. import (
    as_json,
    capture,
    default,
    index,
    name,
    noop,
    to_count,
    to_group,
    to_lower,
    to_reversed,
    to_sorted,
    to_split,
    to_unique,
    to_upper,
)
from ..bases.lookup_encoder_base import LookupEncoderBase
# pylint: disable=wildcard-import,unused-wildcard-import
from .scenarios import *

if TYPE_CHECKING:  # no cover
  from text_lint.__helpers__.operations import AliasParameterDefinitions
  from ..bases.lookup_base import AliasLookupParams


@pytest.fixture
def base_parameter_definitions() -> "AliasParameterDefinitions":
  return {
      "lookup_name": LookupBase.Parameters.lookup_name,
      "lookup_params": LookupBase.Parameters.lookup_params,
  }


def create_result_tree_mock(value: str, children_count: int) -> mock.Mock:
  instance = mock.Mock(spec=ResultTree)
  instance.value = value
  instance.children = []
  for child_index in range(0, children_count):
    child = mock.Mock(spec=ResultTree)
    child.value = str(child_index)
    instance.children.append(child)
  return instance


@pytest.fixture
def mocked_state() -> mock.Mock:
  instance = mock.Mock()
  instance.results = None
  return instance


@pytest.fixture
def mocked_default_subclasses(
    monkeypatch: pytest.MonkeyPatch,
) -> Dict[str, mock.Mock]:
  instances = {
      "IndexLookup": mock.Mock(),
      "NameLookup": mock.Mock(),
  }
  for lookup_name, mock_instance in instances.items():
    monkeypatch.setattr(
        default,
        lookup_name,
        mock_instance,
    )
  return instances


@pytest.fixture
def mocked_encode_method() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_lookup_name() -> str:
  return "mocked_lookup_name"


@pytest.fixture
def mocked_requesting_operation_name() -> str:
  return "mocked_requesting_operation_name"


@pytest.fixture
def mocked_lookup_expression() -> mock.Mock:
  instance = mock.Mock()
  instance.lookups = [mock.Mock(), mock.Mock()]
  return instance


@pytest.fixture
def mocked_trees_grove() -> List[List[mock.Mock]]:
  mocked_tree1 = create_result_tree_mock("A", 3)
  mocked_tree2 = create_result_tree_mock("A", 3)
  return [[mocked_tree1, mocked_tree2]]


@pytest.fixture
def mocked_trees_woods() -> List[List[mock.Mock]]:
  mocked_tree1 = create_result_tree_mock("A", 0)
  mocked_tree1.children = [
      create_result_tree_mock("AA", 3),
      create_result_tree_mock("BB", 3),
      create_result_tree_mock("CC", 3),
  ]
  mocked_tree2 = create_result_tree_mock("B", 0)
  mocked_tree2.children = [
      create_result_tree_mock("AA", 3),
      create_result_tree_mock("EE", 3),
      create_result_tree_mock("FF", 3),
  ]
  mocked_tree3 = create_result_tree_mock("B", 0)
  mocked_tree3.children = [
      create_result_tree_mock("AA", 3),
      create_result_tree_mock("EE", 3),
      create_result_tree_mock("FF", 3),
  ]
  return [[mocked_tree1], [mocked_tree2, mocked_tree3]]


@pytest.fixture
def setup_encoder_lookup(
    mocked_encode_method: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        LookupEncoderBase,
        "encode",
        mocked_encode_method,
    )

  return setup


@pytest.fixture
def as_json_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
    setup_encoder_lookup: Callable[[], None],
) -> as_json.JsonLookup:
  setup_encoder_lookup()
  return as_json.JsonLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def capture_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
) -> capture.CaptureLookup:
  return capture.CaptureLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def index_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
) -> index.IndexLookup:
  return index.IndexLookup(
      "1",
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def name_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
) -> name.NameLookup:
  return name.NameLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def noop_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
) -> noop.NoopLookup:
  return noop.NoopLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def to_count_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
) -> to_count.CountLookup:
  return to_count.CountLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def to_group_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
) -> to_group.GroupLookup:
  return to_group.GroupLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def to_lower_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
    setup_encoder_lookup: Callable[[], None],
) -> to_lower.LowerLookup:
  setup_encoder_lookup()
  return to_lower.LowerLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def to_reversed_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
) -> to_reversed.ReversedLookup:
  return to_reversed.ReversedLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def to_sorted_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
) -> to_sorted.SortedLookup:
  return to_sorted.SortedLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def to_split_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
) -> to_split.SplitLookup:
  return to_split.SplitLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def to_unique_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
    setup_encoder_lookup: Callable[[], None],
) -> to_unique.UniqueLookup:
  setup_encoder_lookup()
  return to_unique.UniqueLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def to_upper_lookup_instance(
    mocked_lookup_expression: mock.Mock,
    mocked_lookup_name: str,
    mocked_lookup_params: "AliasLookupParams",
    mocked_requesting_operation_name: str,
    setup_encoder_lookup: Callable[[], None],
) -> to_upper.UpperLookup:
  setup_encoder_lookup()
  return to_upper.UpperLookup(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_lookup_params,
      mocked_requesting_operation_name,
  )
