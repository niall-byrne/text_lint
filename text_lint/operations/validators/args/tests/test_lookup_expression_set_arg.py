"""Test the LookupExpressionSetArgSetArg class."""

from typing import Any, Dict, List, Union, cast

import pytest
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOKUP_SENTINEL, LOOKUP_SEPERATOR
from text_lint.operations.lookups import CaptureLookup, JsonLookup, UpperLookup
from text_lint.operations.lookups.bases.lookup_base import AliasLookupParams
from text_lint.operations.lookups.parsers.lookup_expressions import (
    ParsedLookup,
)
from ..lookup_expression import (
    AliasYamlLookupExpressionSet,
    LookupExpression,
    LookupExpressionSetArg,
)

AliasParsedLookupDefinition = Dict[str, Union[str, AliasLookupParams]]


class TestLookupExpressionSetArgSetArg:
  """Test the LookupExpressionSetArgSetArg class."""

  def assert_is_lookup_expression_set(
      self,
      instance: Any,
      name: str,
      source: str,
      lookups: List["AliasParsedLookupDefinition"],
  ) -> None:
    assert isinstance(instance, LookupExpression)
    assert instance.name == name
    assert instance.source == source
    assert len(instance.lookups) == len(lookups)
    for lookup, definition in zip(instance.lookups, lookups):
      assert isinstance(lookup, ParsedLookup)
      assert lookup.name == definition["name"]
      assert lookup.params == definition["params"]

  def test_intialize__attributes(
      self,
      lookup_expression_set_instances: List[LookupExpression],
  ) -> None:
    instance = LookupExpressionSetArg(
        lookup_expression_set=lookup_expression_set_instances
    )

    results = list(instance)
    self.assert_is_lookup_expression_set(
        results[0],
        name=LOOKUP_SEPERATOR.join(
            [
                "source1",
                CaptureLookup.operation + "()",
                JsonLookup.operation + "()",
            ]
        ),
        source="source1",
        lookups=[
            {
                "name": CaptureLookup.operation,
                "params": [],
            },
            {
                "name": JsonLookup.operation,
                "params": [],
            },
        ]
    )
    self.assert_is_lookup_expression_set(
        results[1],
        name=LOOKUP_SEPERATOR.join(["source2", UpperLookup.operation + "()"]),
        source="source2",
        lookups=[
            {
                "name": UpperLookup.operation,
                "params": [],
            },
        ]
    )

  def test_intialize__translations(self) -> None:
    assert_is_translated(
        LookupExpressionSetArg.msg_fmt_invalid_lookup_expression_set
    )

  def test_create__no_yaml_definition__does_not_create_instances(self) -> None:
    instance = LookupExpressionSetArg.create([])

    assert len(instance) == 0

  def test_len__multiple_result_sets__returns_expected_value(
      self,
      lookup_expression_set_instances: List[LookupExpression],
  ) -> None:
    instance = LookupExpressionSetArg(
        lookup_expression_set=lookup_expression_set_instances
    )

    assert len(instance) == len(lookup_expression_set_instances)

  def test_create__single_yaml_definition__creates_instance(self) -> None:
    instance = LookupExpressionSetArg.create(
        [
            LOOKUP_SEPERATOR.join(
                [
                    "source1",
                    CaptureLookup.operation + "()",
                    JsonLookup.operation + "()",
                ]
            )
        ]
    )

    results = list(instance)
    assert len(results) == 1
    self.assert_is_lookup_expression_set(
        results[0],
        name=LOOKUP_SEPERATOR.join(
            [
                "source1",
                CaptureLookup.operation + "()",
                JsonLookup.operation + "()",
            ]
        ),
        source="source1",
        lookups=[
            {
                "name": CaptureLookup.operation,
                "params": [],
            },
            {
                "name": JsonLookup.operation,
                "params": [],
            },
        ]
    )

  def test_create__multiple_yaml_definitions__creates_instances(self) -> None:
    instance = LookupExpressionSetArg.create(
        [
            LOOKUP_SEPERATOR.join(
                [
                    "source1",
                    CaptureLookup.operation + "()",
                    JsonLookup.operation + "()",
                ]
            ),
            LOOKUP_SEPERATOR.join(
                [
                    "source2",
                    CaptureLookup.operation + "()",
                    UpperLookup.operation + "()",
                ]
            ),
            "source3",
        ]
    )

    results = list(instance)
    assert len(results) == 3
    self.assert_is_lookup_expression_set(
        results[0],
        name=LOOKUP_SEPERATOR.join(
            [
                "source1",
                CaptureLookup.operation + "()",
                JsonLookup.operation + "()",
            ]
        ),
        source="source1",
        lookups=[
            {
                "name": CaptureLookup.operation,
                "params": [],
            },
            {
                "name": JsonLookup.operation,
                "params": [],
            },
        ]
    )
    self.assert_is_lookup_expression_set(
        results[1],
        name=LOOKUP_SEPERATOR.join(
            [
                "source2",
                CaptureLookup.operation + "()",
                UpperLookup.operation + "()",
            ]
        ),
        source="source2",
        lookups=[
            {
                "name": CaptureLookup.operation,
                "params": [],
            },
            {
                "name": UpperLookup.operation,
                "params": [],
            },
        ]
    )
    self.assert_is_lookup_expression_set(
        results[2],
        name="source3",
        source="source3",
        lookups=[{
            "name": LOOKUP_SENTINEL,
            "params": [],
        }],
    )

  def test_create__invalid_yaml__raises_exception(self) -> None:
    with pytest.raises(TypeError) as exc:
      LookupExpressionSetArg.create(
          cast(AliasYamlLookupExpressionSet, "invalid yaml")
      )

    assert str(exc.value) == (
        LookupExpressionSetArg.msg_fmt_invalid_lookup_expression_set.
        format("invalid yaml")
    )
