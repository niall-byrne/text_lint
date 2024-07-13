"""Shared test fixtures for the validator classes."""
# pylint: disable=redefined-outer-name

from typing import List
from unittest import mock

import pytest
from .. import validate_combine, validate_debug, validate_equal


@pytest.fixture
def mocked_combined_result_tree_name() -> str:
  return "mocked_combined_result_name"


@pytest.fixture
def mocked_controller() -> mock.Mock:
  instance = mock.Mock()
  return instance


@pytest.fixture
def mocked_validator_name() -> str:
  return "mocked_validator_name"


@pytest.fixture
def validate_combine_instance(
    mocked_combined_result_tree_name: str,
    mocked_result_set_a: List[str],
    mocked_validator_name: str,
) -> validate_combine.ValidateCombine:
  return validate_combine.ValidateCombine(
      mocked_validator_name,
      new_saved=mocked_combined_result_tree_name,
      saved=mocked_result_set_a,
  )


@pytest.fixture
def validate_debug_instance(
    mocked_result_set_a: List[str],
    mocked_validator_name: str,
) -> validate_debug.ValidateDebug:
  return validate_debug.ValidateDebug(
      mocked_validator_name,
      saved=mocked_result_set_a,
  )


@pytest.fixture
def validate_equal_instance(
    mocked_result_set_a: List[str],
    mocked_result_set_b: List[str],
    mocked_validator_name: str,
) -> validate_equal.ValidateEqual:
  return validate_equal.ValidateEqual(
      mocked_validator_name,
      saved_a=mocked_result_set_a,
      saved_b=mocked_result_set_b,
  )
