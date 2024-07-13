"""Shared lookup expression test fixtures."""
# pylint: disable=redefined-outer-name

from typing import Dict, List

import pytest
from text_lint.config import LOOKUP_SEPERATOR
from text_lint.operations.lookups import (
    CaptureLookup,
    GroupLookup,
    UpperLookup,
)


@pytest.fixture
def mocked_lookup_expression_set_a() -> List[str]:
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
              GroupLookup.operation,
          ]
      ),
  ]


@pytest.fixture
def mocked_lookup_expression_set_b() -> List[str]:
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
              GroupLookup.operation,
          ]
      ),
  ]


@pytest.fixture
def mocked_lookup_expression_set_c() -> List[str]:
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
              GroupLookup.operation,
          ]
      ),
      LOOKUP_SEPERATOR.join(
          [
              "source7",
              CaptureLookup.operation,
              GroupLookup.operation,
          ]
      ),
  ]


@pytest.fixture
def mocked_lookup_expression_sets(
    mocked_lookup_expression_set_a: List[str],
    mocked_lookup_expression_set_b: List[str],
    mocked_lookup_expression_set_c: List[str],
) -> Dict[str, List[str]]:
  return {
      "a": mocked_lookup_expression_set_a,
      "b": mocked_lookup_expression_set_b,
      "c": mocked_lookup_expression_set_c,
  }
