"""Shared test fixtures for the text_lint sequencer implementation tests."""
# pylint: disable=redefined-outer-name

from io import StringIO
from typing import Dict, List, Type
from unittest import mock

import pytest
from text_lint.sequencers import lookups, rules, textfile, validators


@pytest.fixture
def mocked_file_content(mocked_file_handle: StringIO) -> List[str]:
  mocked_content = ["line %s\n" % line for line in range(0, 10)]
  mocked_file_handle.write("".join(mocked_content))
  mocked_file_handle.seek(0)
  return mocked_content


@pytest.fixture
def mocked_file_content_with_comments(
    mocked_file_handle: StringIO,
) -> List[str]:
  mocked_content = ["line %s\n" % line for line in range(0, 10)]
  mocked_content.insert(0, "# This is a comment\n")
  mocked_content.insert(3, "# This is also comment\n")
  mocked_file_handle.write("".join(mocked_content))
  mocked_file_handle.seek(0)
  return mocked_content


@pytest.fixture
def mocked_file_handle() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_result_set(
    mocked_lookup_registry: Dict[str, mock.Mock],
) -> mock.Mock:
  instance = mock.Mock()
  instance.source = "mocked_result_set_source"
  instance.lookups = list(mocked_lookup_registry.keys())
  return instance


@pytest.fixture
def mocked_lookup_registry() -> Dict[str, mock.Mock]:
  return {
      "A": mock.Mock(),
      "B": mock.Mock(),
      "C": mock.Mock(),
  }


@pytest.fixture
def mocked_open() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_schema() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_textfile() -> str:
  return "mock.makefile"


@pytest.fixture
def lookups_sequencer_class(
    mocked_lookup_registry: Dict[str, mock.Mock],
    monkeypatch: pytest.MonkeyPatch,
) -> Type[lookups.LookupsSequencer]:
  monkeypatch.setattr(
      lookups,
      "lookup_registry",
      mocked_lookup_registry,
  )
  return lookups.LookupsSequencer


@pytest.fixture
def rule_sequencer_class() -> Type[rules.RuleSequencer]:
  return rules.RuleSequencer


@pytest.fixture
def textfile_sequencer_class(
    mocked_file_handle: StringIO,
    mocked_open: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[textfile.TextFileSequencer]:
  monkeypatch.setattr(
      "builtins.open",
      mocked_open,
  )
  mocked_open.return_value = mocked_file_handle
  return textfile.TextFileSequencer


@pytest.fixture
def validator_sequencer_class() -> Type[validators.ValidatorSequencer]:
  return validators.ValidatorSequencer
