"""Shared test fixtures for the text_lint linter tests."""
# pylint: disable=redefined-outer-name

from typing import Callable, List
from unittest import mock

import pytest
from text_lint import linter
from text_lint.linter import recursion, settings
from text_lint.sequencers.patterns.linear import LinearPattern
# pylint: disable=wildcard-import,unused-wildcard-import
from .scenarios import *

AliasLinterSetup = Callable[[], None]


@pytest.fixture
def mocked_file_path() -> str:
  return "mocked_file_path"


@pytest.fixture
def mocked_logger() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_linter() -> mock.Mock:
  instance = mock.Mock(unsafe=True)
  instance.textfile.path = "mocked_file_path"
  return instance


@pytest.fixture
def mocked_recursion_detection() -> mock.Mock:
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
  instance = mock.MagicMock()
  instance.return_value.pattern = LinearPattern()
  return instance


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
    setup_linter_attribute_mocks: AliasLinterSetup,
    setup_linter_sequencer_mocks: AliasLinterSetup,
) -> None:
  setup_linter_attribute_mocks()
  setup_linter_sequencer_mocks()


@pytest.fixture
def setup_linter_attribute_mocks(
    mocked_recursion_detection: mock.Mock,
    mocked_logger: mock.Mock,
    mocked_result_forest: mock.Mock,
    mocked_schema: mock.Mock,
    mocked_state_factory: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:

    monkeypatch.setattr(
        linter,
        "RecursionDetection",
        mocked_recursion_detection,
    )
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
) -> AliasLinterSetup:

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
    setup_linter_attribute_mocks: AliasLinterSetup,
    setup_linter_sequencer_mocks: AliasLinterSetup,
) -> linter.Linter:
  setup_linter_attribute_mocks()
  setup_linter_sequencer_mocks()
  linter_settings = settings.LinterSettings(
      file_path=mocked_file_path,
      interpolate_schema=False,
      quiet=False,
      schema_path=mocked_schema_path,
  )
  return linter.Linter(settings=linter_settings)


@pytest.fixture
def recursion_detection_instance(
    mocked_linter: mock.Mock
) -> recursion.RecursionDetection:
  return recursion.RecursionDetection(mocked_linter)
