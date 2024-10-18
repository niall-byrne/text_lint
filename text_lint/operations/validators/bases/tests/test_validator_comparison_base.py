"""Test the ValidationComparisonBase class."""

from typing import Dict, List, Type
from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
    assert_parameter_schema,
    spy_on_validate_parameters,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.__helpers__.validators import (
    assert_is_invalid_comparison,
    assert_is_validation_failure,
)
from text_lint.exceptions.validators import (
    ValidationFailure,
    ValidationInvalidComparison,
)
from text_lint.operations.validators.args.lookup_expression import (
    LookupExpressionSetArg,
)
from ..validator_base import ValidatorBase
from ..validator_comparison_base import ValidationComparisonBase


class TestValidationComparisonBase:
  """Test the ValidationComparisonBase class."""

  def test_initialize__defined__attributes(
      self,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
      mocked_validator_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "mocked_validator_comparison_base_hint",
        "internal_use_only": False,
        "name": mocked_validator_name,
        "operation": "mocked_validator_comparison_base_operation",
        "yaml_example": "mocked_validator_comparison_base_yaml_example",
    }

    assert_operation_attributes(
        concrete_validator_comparison_base_instance,
        attributes,
    )

  def test_initialize__translations(
      self,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    assert_is_translated(
        concrete_validator_comparison_base_instance.msg_fmt_comparison_failure
    )
    assert_is_translated(
        concrete_validator_comparison_base_instance.msg_fmt_comparison_success
    )
    assert_is_translated(
        concrete_validator_comparison_base_instance.
        msg_fmt_invalid_comparison_description
    )
    assert_is_translated(
        concrete_validator_comparison_base_instance.
        msg_fmt_invalid_comparison_detail
    )
    assert_is_translated(
        concrete_validator_comparison_base_instance.
        msg_fmt_set_count_failure_description
    )
    assert_is_translated(
        concrete_validator_comparison_base_instance.
        msg_fmt_set_count_failure_detail
    )

  def test_initialize__inheritance(
      self,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    assert_operation_inheritance(
        concrete_validator_comparison_base_instance,
        bases=(
            ValidatorBase,
            ValidationComparisonBase,
        ),
    )

  @spy_on_validate_parameters(ValidationComparisonBase)
  def test_initialize__parameter_validation(
      self,
      validate_parameters_spy: mock.Mock,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    assert_parameter_schema(
        instance=concrete_validator_comparison_base_instance,
        parameter_definitions={"name": {
            "type": str
        }}
    )
    validate_parameters_spy.assert_called_once_with(
        concrete_validator_comparison_base_instance
    )

  def test_initialize__creates_result_set_arg_a_instance(
      self,
      mocked_lookup_expression_set_a: List[str],
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    assert isinstance(
        concrete_validator_comparison_base_instance.lookup_expression_set_a,
        LookupExpressionSetArg
    )

    requested_results = list(
        concrete_validator_comparison_base_instance.lookup_expression_set_a
    )
    assert requested_results[0].name == mocked_lookup_expression_set_a[0]
    assert requested_results[1].name == mocked_lookup_expression_set_a[1]

  def test_initialize__creates_result_set_arg_b_instance(
      self,
      mocked_lookup_expression_set_b: List[str],
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    assert isinstance(
        concrete_validator_comparison_base_instance.lookup_expression_set_b,
        LookupExpressionSetArg
    )

    requested_results = list(
        concrete_validator_comparison_base_instance.lookup_expression_set_b
    )
    assert requested_results[0].name == mocked_lookup_expression_set_b[0]
    assert requested_results[1].name == mocked_lookup_expression_set_b[1]

  def test_apply__valid_lookups__performs_each_expected_a_lookup(
      self,
      mocked_state: mock.Mock,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    concrete_validator_comparison_base_instance.apply(mocked_state)

    requested_results = list(
        concrete_validator_comparison_base_instance.lookup_expression_set_a
    )
    assert mocked_state.lookup_expression.call_count == (
        len(requested_results) * 2
    )
    assert mocked_state.lookup_expression.mock_calls[0] == mock.call(
        requested_results[0],
    )
    assert mocked_state.lookup_expression.mock_calls[2] == mock.call(
        requested_results[1],
    )

  def test_apply__valid_lookups__performs_each_expected_b_lookup(
      self,
      mocked_state: mock.Mock,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    concrete_validator_comparison_base_instance.apply(mocked_state)

    requested_results = list(
        concrete_validator_comparison_base_instance.lookup_expression_set_b
    )
    assert mocked_state.lookup_expression.call_count == (
        len(requested_results) * 2
    )
    assert mocked_state.lookup_expression.mock_calls[1] == mock.call(
        requested_results[0],
    )
    assert mocked_state.lookup_expression.mock_calls[3] == mock.call(
        requested_results[1],
    )

  def test_apply__comparison_passes__does_not_raise_exception(
      self,
      mocked_state: mock.Mock,
      mocked_comparison: mock.Mock,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    mocked_comparison.return_value = True

    concrete_validator_comparison_base_instance.apply(mocked_state)

  def test_apply__comparison_passes__logs_expected_lookup_results(
      self,
      mocked_state: mock.Mock,
      mocked_comparison: mock.Mock,
      mocked_lookup_expression_sets: Dict[str, List[str]],
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    mocked_comparison.return_value = True

    concrete_validator_comparison_base_instance.apply(mocked_state)

    assert mocked_state.log.mock_calls == [
        call for call_group in [
            [
                mock.call(
                    concrete_validator_comparison_base_instance.
                    msg_fmt_comparison_success.format(
                        mock_result,
                        mocked_lookup_expression_sets["b"][index],
                    ),
                    indent=True,
                ),
            ] for index, mock_result in
            enumerate(mocked_lookup_expression_sets["a"])
        ] for call in call_group
    ]

  def test_apply__comparison_fails__raises_exception(
      self,
      mocked_state: mock.Mock,
      mocked_comparison: mock.Mock,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    mocked_comparison.return_value = False

    with pytest.raises(ValidationFailure) as exc:
      concrete_validator_comparison_base_instance.apply(mocked_state)

    requested_result_a_name = list(
        concrete_validator_comparison_base_instance.lookup_expression_set_a
    )[0].name
    requested_result_b_name = list(
        concrete_validator_comparison_base_instance.lookup_expression_set_b
    )[0].name
    assert_is_validation_failure(
        exc,
        description_t=(
            concrete_validator_comparison_base_instance.
            msg_fmt_comparison_failure,
            requested_result_a_name,
            requested_result_b_name,
        ),
        detail_t=(
            concrete_validator_comparison_base_instance.
            msg_fmt_comparison_failure,
            mocked_state.lookup_expression.return_value,
            mocked_state.lookup_expression.return_value,
        ),
        validator=concrete_validator_comparison_base_instance,
    )

  def test_apply__comparison_type_error__raises_exception(
      self,
      mocked_state: mock.Mock,
      mocked_comparison: mock.Mock,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    mocked_comparison.side_effect = TypeError

    with pytest.raises(ValidationInvalidComparison) as exc:
      concrete_validator_comparison_base_instance.apply(mocked_state)

    assert_is_invalid_comparison(
        exc,
        description_t=(
            concrete_validator_comparison_base_instance.
            msg_fmt_invalid_comparison_description,
            list(
              concrete_validator_comparison_base_instance. \
              lookup_expression_set_a
            )[0].name,
            list(
              concrete_validator_comparison_base_instance. \
              lookup_expression_set_b
            )[0].name,
        ),
        detail_t=(
            concrete_validator_comparison_base_instance.
            msg_fmt_invalid_comparison_detail,
            str(type(mocked_state.lookup_expression.return_value)),
            str(type(mocked_state.lookup_expression.return_value)),
        ),
        validator=concrete_validator_comparison_base_instance,
    )

  def test_apply__unequal_result_set_counts__raises_exception(
      self,
      mocked_state: mock.Mock,
      mocked_lookup_expression_sets: Dict[str, List[str]],
      concrete_validator_comparison_base_class: Type[ValidationComparisonBase],
  ) -> None:
    instance = concrete_validator_comparison_base_class(
        "mocked_validator",
        saved_a=mocked_lookup_expression_sets["a"],
        saved_b=mocked_lookup_expression_sets["c"],
    )

    with pytest.raises(ValidationFailure) as exc:
      instance.apply(mocked_state)

    assert_is_validation_failure(
        exc,
        description_t=(
            instance.msg_fmt_set_count_failure_description,
            len(mocked_lookup_expression_sets["a"]),
            len(mocked_lookup_expression_sets["c"]),
        ),
        detail_t=(instance.msg_fmt_set_count_failure_detail,),
        validator=instance,
    )
