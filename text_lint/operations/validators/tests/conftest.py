"""Shared test fixtures for the validator classes."""
# pylint: disable=redefined-outer-name

from typing import List
from unittest import mock

import pytest
from .. import validate_debug, validate_equal
# pylint: disable=wildcard-import,unused-wildcard-import
from .scenarios import *


@pytest.fixture
def mocked_state() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_validator_name() -> str:
  return "mocked_validator_name"


@pytest.fixture
def validate_debug_instance(
    mocked_lookup_expression_set_a: List[str],
    mocked_validator_name: str,
) -> validate_debug.ValidateDebug:
  return validate_debug.ValidateDebug(
      mocked_validator_name,
      saved=mocked_lookup_expression_set_a,
  )


@pytest.fixture
def validate_equal_instance(
    mocked_lookup_expression_set_a: List[str],
    mocked_lookup_expression_set_b: List[str],
    mocked_validator_name: str,
) -> validate_equal.ValidateEqual:
  return validate_equal.ValidateEqual(
      mocked_validator_name,
      saved_a=mocked_lookup_expression_set_a,
      saved_b=mocked_lookup_expression_set_b,
  )
