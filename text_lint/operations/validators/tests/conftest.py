"""Shared test fixtures for the validator classes."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, List
from unittest import mock

import pytest
from .. import validate_debug

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.__fixtures__.mocks import AliasMethodMocker
  from text_lint.controller import Controller


@pytest.fixture
def mocked_controller() -> mock.Mock:
  instance = mock.Mock()
  return instance


@pytest.fixture
def mocked_result_set() -> List[str]:
  return [
      "source1.capture.to_upper",
      "source2.capture.to_json",
  ]


@pytest.fixture
def mocked_validator_name() -> str:
  return "mocked_lookup_name"


@pytest.fixture
def validate_debug_instance(
    mocked_result_set: List[str],
    mocked_validator_name: str,
) -> validate_debug.ValidateDebug:
  return validate_debug.ValidateDebug(
      mocked_validator_name,
      mocked_result_set,
  )
