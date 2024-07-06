"""Test fixtures for the text_lint parser rules."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, List, NamedTuple
from unittest import mock

import pytest
from .. import (
    assert_blank,
    assert_equal,
    assert_regex,
    assert_regex_section,
    assert_sequence_begins,
    assert_sequence_ends,
)

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.rules.bases.rule_base import RuleBase
  from text_lint.schema import AliasYamlOperation


class CaseSensitivityScenario(NamedTuple):
  sensitive: bool
  text: str


@pytest.fixture
def mocked_controller(
    mocked_rule_sequencer: mock.MagicMock,
    mocked_textfile: mock.MagicMock,
) -> mock.Mock:
  instance = mock.Mock()
  instance.rules = mocked_rule_sequencer
  instance.textfile = mocked_textfile
  return instance


@pytest.fixture
def mocked_nested_rules() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_operation_definitions(
    mocked_nested_rules: List[mock.Mock]
) -> List["AliasYamlOperation"]:
  return [
      {
          "definition": 1,
          "rules": mocked_nested_rules
      },
      {
          "definition": 2,
          "rules": mocked_nested_rules
      },
  ]


@pytest.fixture
def mocked_operation_instances() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_rule_sequencer() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_schema() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_textfile() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def assert_blank_instance() -> assert_blank.AssertBlank:
  return assert_blank.AssertBlank(name="example assert blank rule")


@pytest.fixture
def assert_equal_instance() -> assert_equal.AssertEqual:
  return assert_equal.AssertEqual(
      name="example assert equal rule",
      expected="#!/usr/bin/make -f\n",
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
      name="example assert regex rule",
      regex="^([a-z-]+):\\s.+\n$",
      save="example",
      splits=[{
          "group": 1,
          "separator": " "
      }],
  )


@pytest.fixture
def assert_regex_section_instance() -> assert_regex_section.AssertRegexSection:
  return assert_regex_section.AssertRegexSection(
      name="example assert regex section rule",
      regex="^([a-z-]+):\\s(.+)\n$",
      save="example",
      splits=[{
          "group": 2
      }],
  )


@pytest.fixture
def assert_sequence_begins_instance(
    mocked_nested_rules: "List[RuleBase]",
) -> assert_sequence_begins.AssertSequenceBegins:
  return assert_sequence_begins.AssertSequenceBegins(
      name="example assert sequence begins rule",
      rules=mocked_nested_rules,
      count=2,
  )


@pytest.fixture
def assert_sequence_ends_instance() -> assert_sequence_ends.AssertSequenceEnds:
  return assert_sequence_ends.AssertSequenceEnds(
      name="example assert sequence ends rule",
  )
