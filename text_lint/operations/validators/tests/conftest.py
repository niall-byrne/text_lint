"""Shared test fixtures for the validator classes."""
# pylint: disable=redefined-outer-name

from typing import List
from unittest import mock

import pytest
from .. import validate_debug


@pytest.fixture
def mocked_state() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_lookup_expression_set() -> List[str]:
  return [
      "source1.capture.to_upper",
      "source2.capture.to_group",
  ]


@pytest.fixture
def mocked_validator_name() -> str:
  return "mocked_lookup_name"


@pytest.fixture
def validate_debug_instance(
    mocked_lookup_expression_set: List[str],
    mocked_validator_name: str,
) -> validate_debug.ValidateDebug:
  return validate_debug.ValidateDebug(
      mocked_validator_name,
      mocked_lookup_expression_set,
  )
