"""Test the LookupExpressionSetArgSetArg class."""

from typing import Any, List

from text_lint.config import LOOKUP_SENTINEL, LOOKUP_SEPERATOR
from text_lint.operations.lookups import CaptureLookup, JsonLookup, UpperLookup
from ..lookup_expression import LookupExpression, LookupExpressionSetArg


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
