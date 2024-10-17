"""Test fixtures for the text_lint assertion operations."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, List, NamedTuple
from unittest import mock

import pytest
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from .. import (
    assert_blank,
    assert_equal,
    assert_regex,
    assert_regex_section,
    assert_sequence_begins,
    assert_sequence_ends,
)

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.__helpers__.operations import AliasParameterDefinitions
  from text_lint.schema import AliasYamlOperation


class CaseSensitivityScenario(NamedTuple):
  sensitive: bool
  text: str


@pytest.fixture
def base_parameter_definitions() -> "AliasParameterDefinitions":
  return {
      "name": AssertionBase.Parameters.name,
      "save": AssertionBase.Parameters.save,
  }


@pytest.fixture
def mocked_state() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_nested_assertions() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_operation_definitions(
    mocked_nested_assertions: mock.Mock
) -> List["AliasYamlOperation"]:
  return [
      {
          "definition": 1,
          "assertions": mocked_nested_assertions
      },
      {
          "definition": 2,
          "assertions": mocked_nested_assertions
      },
  ]


@pytest.fixture
def mocked_operation_instances() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_schema() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def assert_blank_instance() -> assert_blank.AssertBlank:
  return assert_blank.AssertBlank(name="example assert blank assertion")


@pytest.fixture
def assert_equal_instance() -> assert_equal.AssertEqual:
  return assert_equal.AssertEqual(
      name="example assert equal assertion",
      expected="#!/usr/bin/make -f",
      save="example",
      splits=[{
          "group": 1,
          "separator": "/"
      }],
      case_sensitive=False,
  )


@pytest.fixture
def assert_regex_instance() -> assert_regex.AssertRegex:
  return assert_regex.AssertRegex(
      name="example assert regex assertion",
      regex="^([a-z-]+):\\s.+$",
      save="example",
      splits=[{
          "group": 1,
          "separator": " "
      }],
  )


@pytest.fixture
def assert_regex_section_instance() -> assert_regex_section.AssertRegexSection:
  return assert_regex_section.AssertRegexSection(
      name="example assert regex section assertion",
      regex="^([a-z-]+):\\s(.+)$",
      save="example",
      splits=[{
          "group": 2
      }],
  )


@pytest.fixture
def assert_sequence_begins_instance(
    mocked_nested_assertions: "List[AssertionBase]",
) -> assert_sequence_begins.AssertSequenceBegins:
  return assert_sequence_begins.AssertSequenceBegins(
      name="example assert sequence begins assertion",
      assertions=mocked_nested_assertions,
      count=2,
  )


@pytest.fixture
def assert_sequence_ends_instance() -> assert_sequence_ends.AssertSequenceEnds:
  return assert_sequence_ends.AssertSequenceEnds(
      name="example assert sequence ends assertion",
  )
