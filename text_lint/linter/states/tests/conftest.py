"""Test fixtures for the text_lint linter state classes."""
# pylint: disable=redefined-outer-name

from typing import List
from unittest import mock

import pytest
from .. import assertion, lookup, validator


@pytest.fixture
def mocked_assertions() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_linter(mocked_textfile: mock.MagicMock) -> mock.Mock:
  instance = mock.Mock(unsafe=True)
  instance.textfile = mocked_textfile
  return instance


@pytest.fixture
def mocked_textfile() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def assertion_state_instance(
    mocked_linter: mock.Mock,
) -> assertion.AssertionState:
  return assertion.AssertionState(mocked_linter)


@pytest.fixture
def lookup_state_instance(mocked_linter: mock.Mock,) -> lookup.LookupState:
  return lookup.LookupState(mocked_linter)


@pytest.fixture
def validator_state_instance(
    mocked_linter: mock.Mock,
) -> validator.ValidatorState:
  return validator.ValidatorState(mocked_linter)
