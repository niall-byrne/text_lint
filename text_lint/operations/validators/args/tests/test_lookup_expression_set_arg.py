"""Test the LookupExpressionSetArgSetArg class."""

from typing import Any, List, cast

import pytest
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOKUP_SENTINEL, LOOKUP_SEPERATOR
from text_lint.operations.lookups import CaptureLookup, JsonLookup, UpperLookup
from ..lookup_expression import (
    AliasYamlLookupExpressionSet,
    LookupExpression,
    LookupExpressionSetArg,
)


class TestLookupExpressionSetArgSetArg:
  """Test the LookupExpressionSetArgSetArg class."""

  def assert_is_lookup_expression_set(
      self,
      instance: Any,
      name: str,
      source: str,
      lookups: List[str],
  ) -> None:
    assert isinstance(instance, LookupExpression)
    assert instance.name == name
    assert instance.source == source
    assert instance.lookups == lookups

  def test_intialize__attributes(
      self,
      lookup_expression_set_instances: List[LookupExpression],
  ) -> None:
    instance = LookupExpressionSetArg(
        lookup_expression_set=lookup_expression_set_instances
    )

    results = list(instance)
    assert len(results) == len(lookup_expression_set_instances)
    self.assert_is_lookup_expression_set(
        results[0],
        name=LOOKUP_SEPERATOR.join(
            [
                "source1",
                CaptureLookup.operation,
                JsonLookup.operation,
            ]
        ),
        source="source1",
        lookups=[CaptureLookup.operation, JsonLookup.operation]
    )
    self.assert_is_lookup_expression_set(
        results[1],
        name=LOOKUP_SEPERATOR.join(["source2", UpperLookup.operation]),
        source="source2",
        lookups=[UpperLookup.operation]
    )

  def test_intialize__translations(self) -> None:
    assert_is_translated(
        LookupExpressionSetArg.msg_fmt_invalid_lookup_expression_set
    )

  def test_create__no_yaml_definition__does_not_create_instances(self) -> None:
    instance = LookupExpressionSetArg.create([])

    results = list(instance)
    assert len(results) == 0

  def test_create__single_yaml_definition__creates_instance(self) -> None:
    instance = LookupExpressionSetArg.create(
        [
            LOOKUP_SEPERATOR.join(
                [
                    "source1",
                    CaptureLookup.operation,
                    JsonLookup.operation,
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
                CaptureLookup.operation,
                JsonLookup.operation,
            ]
        ),
        source="source1",
        lookups=[CaptureLookup.operation, JsonLookup.operation]
    )

  def test_create__multiple_yaml_definitions__creates_instances(self) -> None:
    instance = LookupExpressionSetArg.create(
        [
            LOOKUP_SEPERATOR.join(
                [
                    "source1",
                    CaptureLookup.operation,
                    JsonLookup.operation,
                ]
            ),
            LOOKUP_SEPERATOR.join(
                [
                    "source2",
                    CaptureLookup.operation,
                    UpperLookup.operation,
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
                CaptureLookup.operation,
                JsonLookup.operation,
            ]
        ),
        source="source1",
        lookups=[CaptureLookup.operation, JsonLookup.operation]
    )
    self.assert_is_lookup_expression_set(
        results[1],
        name=LOOKUP_SEPERATOR.join(
            [
                "source2",
                CaptureLookup.operation,
                UpperLookup.operation,
            ]
        ),
        source="source2",
        lookups=[CaptureLookup.operation, UpperLookup.operation]
    )
    self.assert_is_lookup_expression_set(
        results[2],
        name="source3",
        source="source3",
        lookups=[LOOKUP_SENTINEL],
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
