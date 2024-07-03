"""Test the ReversedLookup class."""

from typing import TYPE_CHECKING
from unittest import mock

from text_lint.__helpers__.lookups import result_reversing_test_cases
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.operations.lookups.encoders.reversed import ReversedEncoder
from ..bases.lookup_base import LookupBase
from ..bases.lookup_encoder_base import LookupEncoderBase
from ..to_reversed import YAML_EXAMPLE, ReversedLookup

if TYPE_CHECKING:  # pragma: no-cover
  from text_lint.results.forest import AliasLookupResult


class TestReversedLookup:
  """Test the ReversedLookup class."""

  def test_initialize__defined__attributes(
      self,
      to_reversed_lookup_instance: ReversedLookup,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "encoder_class": ReversedEncoder,
        "hint": "reverse the order of the saved results",
        "lookup_name": mocked_lookup_name,
        "operation": LOOKUP_TRANSFORMATION_PREFIX + "reversed",
        "requesting_operation_name": mocked_requesting_operation_name,
        "result_set": mocked_result_set,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(to_reversed_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      to_reversed_lookup_instance: ReversedLookup,
  ) -> None:
    assert_is_translated(to_reversed_lookup_instance.hint)

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

  @result_reversing_test_cases
  def test_apply__vary_forest_lookup_results__updates_forest_lookup_results(
      self,
      to_reversed_lookup_instance: ReversedLookup,
      mocked_controller: mock.Mock,
      result: "AliasLookupResult",
      expected: "AliasLookupResult",
  ) -> None:
    mocked_controller.forest.lookup_results = result

    to_reversed_lookup_instance.apply(mocked_controller)

    for value_a, value_b in zip(
        mocked_controller.forest.lookup_results,
        expected,
    ):
      assert value_a == value_b

  def test_apply__string_results__updates_forest_lookup_results(
      self,
      to_reversed_lookup_instance: ReversedLookup,
      mocked_controller: mock.Mock,
  ) -> None:
    mocked_controller.forest.lookup_results = "aaccbb"
    to_reversed_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.lookup_results == "bbccaa"
