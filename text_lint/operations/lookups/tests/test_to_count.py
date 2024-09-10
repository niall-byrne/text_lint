"""Test the CountLookup class."""

from typing import TYPE_CHECKING
from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from ..bases.lookup_base import LookupBase
from ..to_count import YAML_EXAMPLE, CountLookup

if TYPE_CHECKING:  # pragma: no-cover
  from text_lint.results.forest import AliasLookupResult


class TestCountLookup:
  """Test the CountLookup class."""

  def test_initialize__defined__attributes(
      self,
      to_count_lookup_instance: CountLookup,
      mocked_lookup_expression: mock.Mock,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "transform a save id into a count of values",
        "internal_use_only": False,
        "is_positional": False,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": mocked_lookup_name,
        "lookup_params": [],
        "operation": LOOKUP_TRANSFORMATION_PREFIX + "count",
        "requesting_operation_name": mocked_requesting_operation_name,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(to_count_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      to_count_lookup_instance: CountLookup,
  ) -> None:
    assert_is_translated(to_count_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      to_count_lookup_instance: CountLookup,
  ) -> None:
    assert_operation_inheritance(
        to_count_lookup_instance,
        bases=(
            LookupBase,
            CountLookup,
        ),
    )

  @pytest.mark.parametrize(
      "results", [
          {
              "one": "one",
              "two": "two",
              "three": "three"
          },
          ["one", "two", "three"],
          "123",
      ]
  )
  def test_apply__vary_forest_lookup_results__updates_forest_lookup_results(
      self,
      to_count_lookup_instance: CountLookup,
      mocked_state: mock.Mock,
      results: "AliasLookupResult",
  ) -> None:
    mocked_state.results = results

    to_count_lookup_instance.apply(mocked_state)

    assert mocked_state.results == "3"
