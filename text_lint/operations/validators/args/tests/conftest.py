"""Test fixtures for the lookup expression classes."""
# pylint: disable=redefined-outer-name

from typing import List
from unittest import mock

import pytest
from text_lint.config import LOOKUP_SEPERATOR
from text_lint.operations.lookups import CaptureLookup, JsonLookup, UpperLookup
from .. import lookup_expression
from ..lookup_expression import LookupExpression


@pytest.fixture
def lookup_expression_set_instances() -> List[LookupExpression]:
  lookup_expression_1 = LookupExpression(
      LOOKUP_SEPERATOR.join(
          [
              "source1",
              CaptureLookup.operation + "()",
              JsonLookup.operation + "()",
          ]
      )
  )
  lookup_expression_2 = LookupExpression(
      LOOKUP_SEPERATOR.join([
          "source2",
          UpperLookup.operation + "()",
      ])
  )
  return [lookup_expression_1, lookup_expression_2]


@pytest.fixture
def mocked_source() -> str:
  return "mocked_source"


@pytest.fixture
def mocked_parsed_lookups() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_parse_lookup_expression(
    mocked_source: str, mocked_parsed_lookups: List[mock.Mock],
    monkeypatch: pytest.MonkeyPatch
) -> mock.Mock:
  instance = mock.Mock(return_value=(mocked_source, mocked_parsed_lookups))
  monkeypatch.setattr(
      lookup_expression,
      "parse_lookup_expression",
      instance,
  )
  return instance
