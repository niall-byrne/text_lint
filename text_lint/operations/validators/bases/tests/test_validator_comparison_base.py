"""Test the ValidationComparisonBase class."""

from typing import TYPE_CHECKING, Dict, List, Type
from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.__helpers__.validators import assert_is_validation_failure
from text_lint.exceptions.validators import ValidationFailure
from text_lint.operations.validators.args.result_set import ResultSetArg
from ..validator_base import ValidationBase
from ..validator_comparison_base import ValidationComparisonBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.__fixtures__.mocks import AliasMethodMocker


class TestValidationComparisonBase:
  """Test the ValidationComparisonBase class."""

  def test_initialize__defined__attributes(
      self,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
      mocked_validator_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "mocked_hint",
        "internal_use_only": False,
        "name": mocked_validator_name,
        "operation": "mocked_operation",
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
            ValidationBase,
            ValidationComparisonBase,
        ),
    )

  def test_initialize__creates_result_set_arg_a_instance(
      self,
      mocked_result_set_a: List[str],
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    assert isinstance(
        concrete_validator_comparison_base_instance.saved_results_a,
        ResultSetArg
    )

    requested_results = list(
        concrete_validator_comparison_base_instance.saved_results_a
    )
    assert requested_results[0].name == mocked_result_set_a[0]
    assert requested_results[1].name == mocked_result_set_a[1]

  def test_initialize__creates_result_set_arg_b_instance(
      self,
      mocked_result_set_b: List[str],
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    assert isinstance(
        concrete_validator_comparison_base_instance.saved_results_b,
        ResultSetArg
    )

    requested_results = list(
        concrete_validator_comparison_base_instance.saved_results_b
    )
    assert requested_results[0].name == mocked_result_set_b[0]
    assert requested_results[1].name == mocked_result_set_b[1]

  def test_apply__valid_lookups__performs_each_expected_a_lookup(
      self,
      mocked_controller: mock.Mock,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    concrete_validator_comparison_base_instance.apply(mocked_controller)

    requested_results = list(
        concrete_validator_comparison_base_instance.saved_results_a
    )
    assert mocked_controller.forest.lookup.call_count == (
        len(requested_results) * 2
    )
    assert mocked_controller.forest.lookup.mock_calls[0] == mock.call(
        mocked_controller,
        requested_results[0],
        concrete_validator_comparison_base_instance.name,
    )
    assert mocked_controller.forest.lookup.mock_calls[2] == mock.call(
        mocked_controller,
        requested_results[1],
        concrete_validator_comparison_base_instance.name,
    )

  def test_apply__valid_lookups__performs_each_expected_b_lookup(
      self,
      mocked_controller: mock.Mock,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    concrete_validator_comparison_base_instance.apply(mocked_controller)

    requested_results = list(
        concrete_validator_comparison_base_instance.saved_results_b
    )
    assert mocked_controller.forest.lookup.call_count == (
        len(requested_results) * 2
    )
    assert mocked_controller.forest.lookup.mock_calls[1] == mock.call(
        mocked_controller,
        requested_results[0],
        concrete_validator_comparison_base_instance.name,
    )
    assert mocked_controller.forest.lookup.mock_calls[3] == mock.call(
        mocked_controller,
        requested_results[1],
        concrete_validator_comparison_base_instance.name,
    )

  def test_apply__comparison_passes__does_not_raise_exception(
      self,
      mocked_controller: mock.Mock,
      mocked_comparison: mock.Mock,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    mocked_comparison.return_value = True

    concrete_validator_comparison_base_instance.apply(mocked_controller)

  def test_apply__comparison_passes__outputs_expected_lookup_results(
      self,
      method_mocker: "AliasMethodMocker",
      mocked_controller: mock.Mock,
      mocked_comparison: mock.Mock,
      mocked_result_sets: Dict[str, List[str]],
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    mocked_comparison.return_value = True
    mocked_print = method_mocker(
        concrete_validator_comparison_base_instance.print
    )

    expected_mock_calls: List[str] = []
    for index, mock_result in enumerate(mocked_result_sets["a"]):
      expected_mock_calls.append(
          concrete_validator_comparison_base_instance.
          msg_fmt_comparison_success.format(
              mock_result,
              mocked_result_sets["b"][index],
          )
      )

    concrete_validator_comparison_base_instance.apply(mocked_controller)

    assert mocked_print.mock_calls == list(map(mock.call, expected_mock_calls))

  def test_apply__comparison_fails__raises_exception(
      self,
      mocked_controller: mock.Mock,
      mocked_comparison: mock.Mock,
      concrete_validator_comparison_base_instance: ValidationComparisonBase,
  ) -> None:
    mocked_comparison.return_value = False

    with pytest.raises(ValidationFailure) as exc:
      concrete_validator_comparison_base_instance.apply(mocked_controller)

    requested_result_a_name = list(
        concrete_validator_comparison_base_instance.saved_results_a
    )[0].name
    requested_result_b_name = list(
        concrete_validator_comparison_base_instance.saved_results_b
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
            mocked_controller.forest.lookup.return_value,
            mocked_controller.forest.lookup.return_value,
        ),
        validator=concrete_validator_comparison_base_instance,
    )

  def test_apply__unequal_result_set_counts__raises_exception(
      self,
      mocked_controller: mock.Mock,
      mocked_result_sets: Dict[str, List[str]],
      concrete_validator_comparison_base_class: Type[ValidationComparisonBase],
  ) -> None:
    instance = concrete_validator_comparison_base_class(
        "mocked_validator",
        saved_a=mocked_result_sets["a"],
        saved_b=mocked_result_sets["c"],
    )

    with pytest.raises(ValidationFailure) as exc:
      instance.apply(mocked_controller)

    assert_is_validation_failure(
        exc,
        description_t=(
            instance.msg_fmt_set_count_failure_description,
            len(mocked_result_sets["a"]),
            len(mocked_result_sets["c"]),
        ),
        detail_t=(instance.msg_fmt_set_count_failure_detail,),
        validator=instance,
    )
