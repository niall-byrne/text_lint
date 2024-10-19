"""Test the ReversedLookup class."""

from typing import TYPE_CHECKING
from unittest import mock

from text_lint.__helpers__.lookups import result_reversing_test_cases
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    AliasParameterDefinitions,
    assert_operation_attributes,
    assert_operation_inheritance,
    assert_parameter_schema,
    spy_on_validate_parameters,
)
from text_lint.__helpers__.translations import (
    assert_is_translated,
    assert_is_translated_yaml_example,
)
from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.operations.lookups.encoders.reversed import ReversedEncoder
from ..bases.lookup_base import LookupBase
from ..bases.lookup_encoder_base import LookupEncoderBase
from ..to_reversed import YAML_EXAMPLE, YAML_EXAMPLE_COMPONENTS, ReversedLookup

if TYPE_CHECKING:  # pragma: no-cover
  from text_lint.results.forest import AliasLookupResult


class TestReversedLookup:
  """Test the ReversedLookup class."""

  def test_initialize__defined__attributes(
      self,
      to_reversed_lookup_instance: ReversedLookup,
      mocked_lookup_expression: mock.Mock,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "encoder_class": ReversedEncoder,
        "hint": "reverse the order of a save id",
        "internal_use_only": False,
        "is_positional": False,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": mocked_lookup_name,
        "lookup_params": [],
        "operation": LOOKUP_TRANSFORMATION_PREFIX + "reversed",
        "requesting_operation_name": mocked_requesting_operation_name,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(to_reversed_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      to_reversed_lookup_instance: ReversedLookup,
  ) -> None:
    assert_is_translated(to_reversed_lookup_instance.hint)
    assert_is_translated_yaml_example(
        to_reversed_lookup_instance.yaml_example,
        YAML_EXAMPLE_COMPONENTS,
    )

  def test_initialize__inheritance(
      self,
      to_reversed_lookup_instance: ReversedLookup,
  ) -> None:
    assert_operation_inheritance(
        to_reversed_lookup_instance,
        bases=(
            LookupBase,
            LookupEncoderBase,
            ReversedLookup,
        ),
    )

  @spy_on_validate_parameters(ReversedLookup)
  def test_initialize__parameter_validation(
      self,
      validate_parameters_spy: mock.Mock,
      to_reversed_lookup_instance: ReversedLookup,
      base_parameter_definitions: "AliasParameterDefinitions",
  ) -> None:
    assert_parameter_schema(
        instance=to_reversed_lookup_instance,
        parameter_definitions=base_parameter_definitions,
    )
    validate_parameters_spy.assert_called_once_with(to_reversed_lookup_instance)

  @result_reversing_test_cases
  def test_apply__vary_forest_lookup_results__updates_forest_lookup_results(
      self,
      to_reversed_lookup_instance: ReversedLookup,
      mocked_state: mock.Mock,
      result: "AliasLookupResult",
      expected: "AliasLookupResult",
  ) -> None:
    mocked_state.results = result

    to_reversed_lookup_instance.apply(mocked_state)

    for value_a, value_b in zip(
        mocked_state.results,
        expected,
    ):
      assert value_a == value_b

  def test_apply__string_results__updates_forest_lookup_results(
      self,
      to_reversed_lookup_instance: ReversedLookup,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.results = "aaccbb"
    to_reversed_lookup_instance.apply(mocked_state)

    assert mocked_state.results == "bbccaa"
