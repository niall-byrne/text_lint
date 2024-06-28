"""Test fixtures for the text_lint linter state base classes."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from .. import state_base


@pytest.fixture
def mocked_linter() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_state_base_instance(
    mocked_linter: mock.Mock,
) -> state_base.StateBase:
  return state_base.StateBase(mocked_linter)
