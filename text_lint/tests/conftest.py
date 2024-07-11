"""Shared test fixtures for the text_lint controller tests."""
# pylint: disable=redefined-outer-name

from typing import Callable, List
from unittest import mock

import pytest
from text_lint import controller


@pytest.fixture
def mocked_file_path() -> str:
  return "mocked_file_path"


@pytest.fixture
def mocked_result_forest() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_rule_sequencer() -> mock.MagicMock:
  instance = mock.MagicMock()
  instance.return_value.pattern = None
  return instance


@pytest.fixture
def mocked_schema() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_schema_path() -> str:
  return "mocked_schema_path"


@pytest.fixture
def mocked_sequence() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_interrupted_rule_sequence(
    mocked_sequence: List[mock.Mock],
) -> List[mock.Mock]:
  mocked_sequence[1].apply.side_effect = StopIteration
  return mocked_sequence


@pytest.fixture
def mocked_text_file_sequencer() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_validator_sequencer() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def setup_controller_mocks(
    mocked_schema: mock.Mock,
    mocked_rule_sequencer: mock.MagicMock,
    mocked_result_forest: mock.Mock,
    mocked_text_file_sequencer: mock.MagicMock,
    mocked_validator_sequencer: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[], None]:

  def setup() -> None:
    monkeypatch.setattr(
        controller,
        "ResultForest",
        mocked_result_forest,
    )
    monkeypatch.setattr(
        controller,
        "RuleSequencer",
        mocked_rule_sequencer,
    )
    monkeypatch.setattr(
        controller,
        "Schema",
        mocked_schema,
    )
    monkeypatch.setattr(
        controller,
        "TextFileSequencer",
        mocked_text_file_sequencer,
    )
    monkeypatch.setattr(
        controller,
        "ValidatorSequencer",
        mocked_validator_sequencer,
    )

  return setup


@pytest.fixture
def controller_instance(
    mocked_file_path: str,
    mocked_schema_path: str,
    setup_controller_mocks: Callable[[], None],
) -> controller.Controller:
  setup_controller_mocks()
  return controller.Controller(
      file_path=mocked_file_path,
      schema_path=mocked_schema_path,
  )
