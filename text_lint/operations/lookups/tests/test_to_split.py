"""Test the SplitLookup class."""

from copy import deepcopy
from typing import TYPE_CHECKING, Any, List, Optional
from unittest import mock

import pytest
from text_lint.__helpers__.lookups import (
    assert_is_lookup_failure,
    result_splitting_test_cases,
)
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
from text_lint.exceptions.lookups import LookupFailure
from text_lint.operations.lookups.encoders.split import SplitEncoder
from text_lint.operations.mixins.parameter_validation import validators
from ..bases.lookup_base import LookupBase
from ..bases.lookup_encoder_base import LookupEncoderBase
from ..to_split import YAML_EXAMPLE, YAML_EXAMPLE_COMPONENTS, SplitLookup

if TYPE_CHECKING:  # pragma: no-cover
  from text_lint.operations.lookups.bases.lookup_base import AliasLookupParams
  from text_lint.results.forest import AliasLookupResult


class TestSplitLookup:
  """Test the SplitLookup class."""

  def test_initialize__defined__attributes(
      self,
      to_split_lookup_instance: SplitLookup,
      mocked_lookup_expression: mock.Mock,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "encoder_class": SplitEncoder,
        "hint": "split the values of a save id",
        "internal_use_only": False,
        "is_positional": False,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": mocked_lookup_name,
        "lookup_params": [],
        "operation": LOOKUP_TRANSFORMATION_PREFIX + "split",
        "requesting_operation_name": mocked_requesting_operation_name,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(to_split_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      to_split_lookup_instance: SplitLookup,
  ) -> None:
    assert_is_translated(to_split_lookup_instance.hint)
    assert_is_translated_yaml_example(
        to_split_lookup_instance.yaml_example,
        YAML_EXAMPLE_COMPONENTS,
    )

  def test_initialize__inheritance(
      self,
      to_split_lookup_instance: SplitLookup,
  ) -> None:
    assert_operation_inheritance(
        to_split_lookup_instance,
        bases=(
            LookupBase,
            LookupEncoderBase,
            SplitLookup,
        ),
    )

  @spy_on_validate_parameters(SplitLookup)
  def test_initialize__parameter_validation(
      self,
      validate_parameters_spy: mock.Mock,
      to_split_lookup_instance: SplitLookup,
      base_parameter_definitions: "AliasParameterDefinitions",
  ) -> None:
    base_parameter_definitions.update(
        {
            "lookup_params":
                {
                    "type":
                        list,
                    "of":
                        str,
                    "validators":
                        [
                            validators.create_is_greater_than_or_equal(
                                0,
                                conversion_function=len,
                            ),
                            validators.create_is_less_than_or_equal(
                                1,
                                conversion_function=len,
                            ),
                        ],
                }
        }
    )

    assert_parameter_schema(
        instance=to_split_lookup_instance,
        parameter_definitions=base_parameter_definitions,
    )
    validate_parameters_spy.assert_called_once_with(to_split_lookup_instance)

  def test_initialize__default_seperator__attribute(
      self,
      to_split_lookup_instance: SplitLookup,
  ) -> None:
    assert to_split_lookup_instance.lookup_params == []
    assert to_split_lookup_instance.seperator is None

  @pytest.mark.parametrize(
      "lookup_params,expected_seperator",
      [
          [[], None],
          [["-"], "-"],
          [[" "], " "],
          [["1"], "1"],
      ],
      ids=lambda p: str(p) if not isinstance(p, str) else "'" + p + "'",
  )
  def test_initialize__vary_valid_params__sets_correct_seperator(
      self,
      mocked_lookup_expression: mock.Mock,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      lookup_params: "AliasLookupParams",
      expected_seperator: Optional[str],
  ) -> None:
    instance = SplitLookup(
        mocked_lookup_name,
        mocked_lookup_expression,
        lookup_params,
        mocked_requesting_operation_name,
    )

    assert instance.seperator == expected_seperator

  @pytest.mark.parametrize("lookup_params", [[1], ["-", " "]])
  def test_initialize__vary_invalid_seperator__raises_exception(
      self,
      to_split_lookup_instance: SplitLookup,
      mocked_lookup_expression: mock.Mock,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      lookup_params: List[Any],
  ) -> None:
    to_split_lookup_instance.lookup_params = lookup_params

    with pytest.raises(LookupFailure) as exc:
      SplitLookup(
          mocked_lookup_name,
          mocked_lookup_expression,
          lookup_params,
          mocked_requesting_operation_name,
      )

    assert_is_lookup_failure(
        exc=exc,
        description_t=(
            SplitLookup.msg_fmt_invalid_parameters,
            lookup_params,
        ),
        lookup=to_split_lookup_instance
    )

  @result_splitting_test_cases
  def test_apply__vary_forest_lookup_results__updates_forest_lookup_results(
      self,
      to_split_lookup_instance: SplitLookup,
      mocked_state: mock.Mock,
      result: "AliasLookupResult",
      seperator: Optional[str],
      expected: "AliasLookupResult",
  ) -> None:
    mocked_state.results = deepcopy(result)
    to_split_lookup_instance.seperator = seperator

    to_split_lookup_instance.apply(mocked_state)

    assert mocked_state.results == expected
