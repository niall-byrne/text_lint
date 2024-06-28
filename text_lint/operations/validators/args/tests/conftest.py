"""Test fixtures for the result set classes."""
from typing import List

import pytest
from text_lint.config import LOOKUP_SEPERATOR
from text_lint.operations.lookups import CaptureLookup, JsonLookup, UpperLookup
from ..result_set import ResultSet


@pytest.fixture
def result_set_instances() -> List[ResultSet]:
  result_set1 = ResultSet(
      LOOKUP_SEPERATOR.join(
          [
              "source1",
              CaptureLookup.operation,
              JsonLookup.operation,
          ]
      )
  )
  result_set2 = ResultSet(
      LOOKUP_SEPERATOR.join([
          "source2",
          UpperLookup.operation,
      ])
  )
  return [result_set1, result_set2]
