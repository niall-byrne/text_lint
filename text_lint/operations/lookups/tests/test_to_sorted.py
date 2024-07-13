"""Test the SortedLookup class."""

from typing import TYPE_CHECKING
from unittest import mock

from text_lint.__helpers__.lookups import result_sorting_test_cases
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.operations.lookups.encoders.sorted import SortedEncoder
from ..bases.lookup_base import LookupBase
from ..bases.lookup_encoder_base import LookupEncoderBase
from ..to_sorted import SortedLookup

if TYPE_CHECKING:  # pragma: no-cover
  from text_lint.results.forest import AliasLookupResult


class TestSortedLookup:
  """Test the SortedLookup class."""

  def test_initialize__defined__attributes(
      self,
      to_sorted_lookup_instance: SortedLookup,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "encoder_class": SortedEncoder,
        "hint": "sort the saved results",
        "lookup_name": mocked_lookup_name,
        "operation": LOOKUP_TRANSFORMATION_PREFIX + "sorted",
        "requesting_operation_name": mocked_requesting_operation_name,
        "result_set": mocked_result_set,
    }

    assert_operation_attributes(to_sorted_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      to_sorted_lookup_instance: SortedLookup,
  ) -> None:
    assert_is_translated(to_sorted_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      to_sorted_lookup_instance: SortedLookup,
  ) -> None:
    assert_operation_inheritance(
        to_sorted_lookup_instance,
        bases=(
            LookupBase,
            LookupEncoderBase,
            SortedLookup,
        ),
    )

  @result_sorting_test_cases
  def test_apply__vary_forest_lookup_results__updates_forest_lookup_results(
      self,
      to_sorted_lookup_instance: SortedLookup,
      mocked_controller: mock.Mock,
      result: "AliasLookupResult",
      expected: "AliasLookupResult",
  ) -> None:
    mocked_controller.forest.lookup_results = result

    to_sorted_lookup_instance.apply(mocked_controller)

    for value_a, value_b in zip(
        mocked_controller.forest.lookup_results,
        expected,
    ):
      assert value_a == value_b

  def test_apply__string_results__updates_forest_lookup_results(
      self,
      to_sorted_lookup_instance: SortedLookup,
      mocked_controller: mock.Mock,
  ) -> None:
    mocked_controller.forest.lookup_results = "gfedcba"

    to_sorted_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.lookup_results == "abcdefg"
