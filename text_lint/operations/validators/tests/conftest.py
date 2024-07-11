"""Shared test fixtures for the validator classes."""
# pylint: disable=redefined-outer-name

from typing import List
from unittest import mock

import pytest
from text_lint.config import LOOKUP_SEPERATOR
from text_lint.operations.lookups import CaptureLookup, JsonLookup, UpperLookup
from .. import validate_debug, validate_equal


@pytest.fixture
def mocked_controller() -> mock.Mock:
  instance = mock.Mock()
  return instance


@pytest.fixture
def mocked_result_set_a() -> List[str]:
  return [
      LOOKUP_SEPERATOR.join(
          [
              "source1",
              CaptureLookup.operation,
              UpperLookup.operation,
          ]
      ),
      LOOKUP_SEPERATOR.join(
          [
              "source2",
              CaptureLookup.operation,
              JsonLookup.operation,
          ]
      ),
  ]


@pytest.fixture
def mocked_result_set_b() -> List[str]:
  return [
      LOOKUP_SEPERATOR.join(
          [
              "source3",
              CaptureLookup.operation,
              UpperLookup.operation,
          ]
      ),
      LOOKUP_SEPERATOR.join(
          [
              "source4",
              CaptureLookup.operation,
              JsonLookup.operation,
          ]
      ),
  ]


@pytest.fixture
def mocked_result_set_c() -> List[str]:
  return [
      LOOKUP_SEPERATOR.join(
          [
              "source5",
              CaptureLookup.operation,
              UpperLookup.operation,
          ]
      ),
      LOOKUP_SEPERATOR.join(
          [
              "source6",
              CaptureLookup.operation,
              JsonLookup.operation,
          ]
      ),
      LOOKUP_SEPERATOR.join(
          [
              "source7",
              CaptureLookup.operation,
              JsonLookup.operation,
          ]
      ),
  ]


@pytest.fixture
def mocked_validator_name() -> str:
  return "mocked_validator_name"


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
