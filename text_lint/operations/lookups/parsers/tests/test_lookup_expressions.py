"""Test the lookup expression parser functions."""

from typing import Dict, List, Type, Union

import pytest
from text_lint.config import LOOKUP_SENTINEL
from text_lint.exceptions.schema import (
    LookupExpressionInvalid,
    LookupExpressionInvalidSequence,
)
from text_lint.operations.lookups.bases.lookup_base import AliasLookupParams
from ..lookup_expressions import ParsedLookup, parse_lookup_expression

AliasParsedLookupDefinition = Dict[str, Union[str, AliasLookupParams]]


class TestParseLookupExpression:
  """Test the parse_lookup_expression function."""

  def assert_are_parsed_lookups(
      self,
      definitions: List["AliasParsedLookupDefinition"],
      parsed_lookups: List[ParsedLookup],
  ) -> None:
    assert len(parsed_lookups) == len(definitions)
    for lookup, definition in zip(parsed_lookups, definitions):
      assert isinstance(lookup, ParsedLookup)
      assert lookup.name == definition["name"]
      assert lookup.params == definition["params"]

  @pytest.mark.parametrize(
      "expression,expected_source,expected_lookups", [
          (
              "~static_value",
              "~static_value",
              [{
                  "name": LOOKUP_SENTINEL,
                  "params": []
              }],
          ),
          (
              "~static_value.as_json().entire_value_is_static",
              "~static_value.as_json().entire_value_is_static",
              [{
                  "name": LOOKUP_SENTINEL,
                  "params": []
              }],
          ), (
              "source1",
              "source1",
              [{
                  "name": LOOKUP_SENTINEL,
                  "params": []
              }],
          ),
          (
              "source2.unknown_lookup()",
              "source2",
              [{
                  "name": "unknown_lookup",
                  "params": []
              }],
          ),
          (
              "source3.capture(1)",
              "source3",
              [{
                  "name": "capture",
                  "params": [1]
              }],
          ),
          (
              "source4.capture(1,2)",
              "source4",
              [{
                  "name": "capture",
                  "params": [1, 2]
              }],
          ),
          (
              "source5.capture(1,2).to_json()",
              "source5",
              [
                  {
                      "name": "capture",
                      "params": [1, 2]
                  },
                  {
                      "name": "to_json",
                      "params": []
                  },
              ],
          )
      ]
  )
  def test__simple_expression__vary_input__returns_source_and_parsed_lookups(
      self,
      expression: str,
      expected_source: str,
      expected_lookups: List["AliasParsedLookupDefinition"],
  ) -> None:
    parsed_source, parsed_lookups = parse_lookup_expression(expression)

    assert parsed_source == expected_source
    self.assert_are_parsed_lookups(
        definitions=expected_lookups,
        parsed_lookups=parsed_lookups,
    )

  @pytest.mark.parametrize(
      "expression,expected_source,expected_lookups", [
          (
              "source6.capture(1,'A','.',')','#').to_json()",
              "source6",
              [
                  {
                      "name": "capture",
                      "params": [1, "A", ".", ")", "#"]
                  },
                  {
                      "name": "to_json",
                      "params": []
                  },
              ],
          ),
          (
              "source7.capture('source7.capture(\"A\").to_json()').to_json()",
              "source7",
              [
                  {
                      "name": "capture",
                      "params": ["source7.capture(\"A\").to_json()"]
                  },
                  {
                      "name": "to_json",
                      "params": []
                  },
              ],
          ),
      ]
  )
  def test__complex_expression__vary_input__returns_source_and_parsed_lookups(
      self,
      expression: str,
      expected_source: str,
      expected_lookups: List["AliasParsedLookupDefinition"],
  ) -> None:
    parsed_source, parsed_lookups = parse_lookup_expression(expression)

    assert parsed_source == expected_source
    self.assert_are_parsed_lookups(
        definitions=expected_lookups,
        parsed_lookups=parsed_lookups,
    )

  @pytest.mark.parametrize(
      "expression,expected_exception", [
          ("source8.to_upper().capture()", LookupExpressionInvalidSequence),
      ]
  )
  def test__invalid_sequence__vary_input__raises_exception(
      self,
      expression: str,
      expected_exception: Type[Exception],
  ) -> None:
    with pytest.raises(expected_exception) as exc:
      _ = parse_lookup_expression(expression)

    assert str(exc.value) == expression

  @pytest.mark.parametrize(
      "expression,expected_exception", [
          ("source9.capture(.capture()", LookupExpressionInvalid),
          ("source9.capture(.capture(", LookupExpressionInvalid),
          ("source10.capture.capture()", LookupExpressionInvalid),
          ("source11.capture(1).to_json()leftovers", LookupExpressionInvalid),
      ]
  )
  def test__invalid_expression__vary_input__raises_exception(
      self,
      expression: str,
      expected_exception: Type[Exception],
  ) -> None:
    with pytest.raises(expected_exception) as exc:
      _ = parse_lookup_expression(expression)

    assert str(exc.value) == expression
