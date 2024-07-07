"""Shared test fixtures for sequencer patterns."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from ..linear import LinearPattern
from ..loop import LinearLoopPattern


@pytest.fixture
def mocked_end_point() -> int:
  return 9


@pytest.fixture
def mocked_sequencer() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_start_point() -> int:
  return 1


@pytest.fixture
def linear_pattern_instance() -> LinearPattern:
  return LinearPattern()


@pytest.fixture
def loop_pattern_instance(
    mocked_end_point: int,
    mocked_start_point: int,
) -> LinearLoopPattern:
  return LinearLoopPattern(
      start=mocked_start_point,
      end=mocked_end_point,
  )
