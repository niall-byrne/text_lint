"""Test scenarios for the linter class."""
# pylint: disable=redefined-outer-name

from typing import List
from unittest import mock

import pytest

__all__ = (
    "scenario__all_text__all_schema__all_assertions",
    "scenario__all_text__all_schema__some_assertions",
    "scenario__all_text__some_schema__all_assertions",
    "scenario__some_text__all_schema__all_assertions",
)


@pytest.fixture
def scenario__all_text__all_schema__all_assertions(
    mocked_sequence_assertions: List[mock.Mock],
    mocked_sequence_validators: List[mock.Mock],
    mocked_sequencer_assertions: mock.MagicMock,
    mocked_sequencer_text_file: mock.Mock,
    mocked_sequencer_validators: mock.MagicMock,
) -> None:
  mocked_sequencer_assertions.return_value.__next__. \
      side_effect = StopIteration
  mocked_sequencer_text_file.return_value.__next__. \
      side_effect = StopIteration
  mocked_sequencer_assertions.return_value.__iter__. \
      return_value = mocked_sequence_assertions
  mocked_sequencer_validators.return_value.__iter__. \
      return_value = mocked_sequence_validators


@pytest.fixture
def scenario__all_text__all_schema__some_assertions(
    mocked_sequence_assertions: List[mock.Mock],
    mocked_sequence_validators: List[mock.Mock],
    mocked_sequencer_assertions: mock.MagicMock,
    mocked_sequencer_text_file: mock.Mock,
    mocked_sequencer_validators: mock.MagicMock,
) -> None:
  mocked_sequencer_assertions.return_value.__next__. \
      side_effect = StopIteration
  mocked_sequencer_text_file.return_value.__next__. \
      side_effect = StopIteration
  mocked_sequencer_assertions.return_value.__iter__. \
      return_value = mocked_sequence_assertions
  mocked_sequencer_validators.return_value.__iter__. \
      return_value = mocked_sequence_validators
  mocked_sequence_assertions[1].apply.side_effect = StopIteration


@pytest.fixture
def scenario__all_text__some_schema__all_assertions(
    mocked_sequence_assertions: List[mock.Mock],
    mocked_sequence_validators: List[mock.Mock],
    mocked_sequencer_assertions: mock.MagicMock,
    mocked_sequencer_text_file: mock.Mock,
    mocked_sequencer_validators: mock.MagicMock,
) -> None:
  mocked_sequencer_text_file.return_value.__next__. \
      side_effect = StopIteration
  mocked_sequencer_assertions.return_value.__iter__. \
      return_value = mocked_sequence_assertions
  mocked_sequencer_validators.return_value.__iter__. \
      return_value = mocked_sequence_validators


@pytest.fixture
def scenario__some_text__all_schema__all_assertions(
    mocked_sequence_assertions: List[mock.Mock],
    mocked_sequence_validators: List[mock.Mock],
    mocked_sequencer_assertions: mock.MagicMock,
    mocked_sequencer_validators: mock.MagicMock,
) -> None:
  mocked_sequencer_assertions.return_value.__next__. \
      side_effect = StopIteration
  mocked_sequencer_assertions.return_value.__iter__. \
      return_value = mocked_sequence_assertions
  mocked_sequencer_validators.return_value.__iter__. \
      return_value = mocked_sequence_validators
