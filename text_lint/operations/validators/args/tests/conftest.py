"""Test fixtures for the result set classes."""
from typing import List

import pytest
from text_lint.config import LOOKUP_SEPERATOR
from text_lint.operations.lookups import CaptureLookup, JsonLookup, UpperLookup
from ..lookup_expression import LookupExpression


@pytest.fixture
def lookup_expression_set_instances() -> List[LookupExpression]:
  lookup_expression_1 = LookupExpression(
      LOOKUP_SEPERATOR.join(
          [
              "source1",
              CaptureLookup.operation,
              JsonLookup.operation,
          ]
      )
  )
  lookup_expression_2 = LookupExpression(
      LOOKUP_SEPERATOR.join([
          "source2",
          UpperLookup.operation,
      ])
  )
  return [lookup_expression_1, lookup_expression_2]
