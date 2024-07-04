"""Shared test fixtures for the text_lint linter tests."""
# pylint: disable=redefined-outer-name

from typing import Callable, List
from unittest import mock

import pytest
from text_lint import linter
from text_lint.linter import settings
# pylint: disable=wildcard-import,unused-wildcard-import
from .scenarios import *


@pytest.fixture
def mocked_file_path() -> str:
  return "mocked_file_path"


@pytest.fixture
def mocked_logger() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_result_forest() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_schema() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_schema_path() -> str:
  return "mocked_schema_path"


@pytest.fixture
def mocked_sequence_assertions() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_sequence_validators() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_sequencer_assertions() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_sequencer_text_file() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_sequencer_validators() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_state_factory() -> mock.Mock:
  return mock.Mock(return_value=mock.Mock(unsafe=True))


@pytest.fixture
def setup_linter_mocks(
    mocked_logger: mock.Mock,
    mocked_result_forest: mock.Mock,
    mocked_schema: mock.Mock,
    mocked_state_factory: mock.Mock,
    setup_linter_sequencer_mocks: Callable[[], None],
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    setup_linter_sequencer_mocks()
    monkeypatch.setattr(
        linter,
        "Logger",
        mocked_logger,
    )
    monkeypatch.setattr(
        linter,
        "ResultForest",
        mocked_result_forest,
    )
    monkeypatch.setattr(
        linter,
        "Schema",
        mocked_schema,
    )
    monkeypatch.setattr(
        linter.states,
        "StateFactory",
        mocked_state_factory,
    )

  return setup


@pytest.fixture
def setup_linter_sequencer_mocks(
    mocked_sequencer_assertions: mock.MagicMock,
    mocked_sequencer_text_file: mock.MagicMock,
    mocked_sequencer_validators: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        linter,
        "AssertionSequencer",
        mocked_sequencer_assertions,
    )
    monkeypatch.setattr(
        linter,
        "TextFileSequencer",
        mocked_sequencer_text_file,
    )
    monkeypatch.setattr(
        linter,
        "ValidatorSequencer",
        mocked_sequencer_validators,
    )

  return setup


@pytest.fixture
def linter_instance(
    mocked_file_path: str,
    mocked_schema_path: str,
    setup_linter_mocks: Callable[[], None],
) -> linter.Linter:
  setup_linter_mocks()
  linter_settings = settings.LinterSettings(
      file_path=mocked_file_path,
      schema_path=mocked_schema_path,
  )
  return linter.Linter(settings=linter_settings)
