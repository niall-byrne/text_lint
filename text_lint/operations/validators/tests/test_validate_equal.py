"""Test the ValidateEqual class."""

from typing import TYPE_CHECKING, Dict, List
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
from ..bases.validator_base import ValidationBase
from ..validate_equal import YAML_EXAMPLE, ValidateEqual

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.__fixtures__.mocks import AliasMethodMocker


class TestValidateEqual:
  """Test the ValidateEqual class."""

  def test_initialize__defined__attributes(
      self,
      validate_equal_instance: ValidateEqual,
      mocked_validator_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "validates equality between sets of values",
        "internal_use_only": False,
        "name": mocked_validator_name,
        "operation": "validate_equal",
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(
        validate_equal_instance,
        attributes,
    )

  def test_initialize__translations(
      self,
      validate_equal_instance: ValidateEqual,
  ) -> None:
    assert_is_translated(validate_equal_instance.hint)
    assert_is_translated(validate_equal_instance.msg_fmt_comparison_failure)
    assert_is_translated(validate_equal_instance.msg_fmt_comparison_success)

  def test_initialize__inheritance(
      self,
      validate_equal_instance: ValidateEqual,
  ) -> None:
    assert_operation_inheritance(
        validate_equal_instance,
        bases=(ValidationBase, ValidateEqual),
    )

  def test_initialize__creates_result_set_arg_a_instance(
      self,
      mocked_result_set_a: List[str],
      validate_equal_instance: ValidateEqual,
  ) -> None:
    assert isinstance(validate_equal_instance.saved_results_a, ResultSetArg)

    requested_results = list(validate_equal_instance.saved_results_a)
    assert requested_results[0].name == mocked_result_set_a[0]
    assert requested_results[1].name == mocked_result_set_a[1]

  def test_initialize__creates_result_set_arg_b_instance(
      self,
      mocked_result_set_b: List[str],
      validate_equal_instance: ValidateEqual,
  ) -> None:
    assert isinstance(validate_equal_instance.saved_results_b, ResultSetArg)

    requested_results = list(validate_equal_instance.saved_results_b)
    assert requested_results[0].name == mocked_result_set_b[0]
    assert requested_results[1].name == mocked_result_set_b[1]

  def test_apply__valid_lookups__performs_each_expected_a_lookup(
      self,
      mocked_controller: mock.Mock,
      validate_equal_instance: ValidateEqual,
  ) -> None:
    validate_equal_instance.apply(mocked_controller)

    requested_results = list(validate_equal_instance.saved_results_a)
    assert mocked_controller.forest.lookup.call_count == (
        len(requested_results) * 2
    )
    assert mocked_controller.forest.lookup.mock_calls[0] == mock.call(
        mocked_controller,
        requested_results[0],
        validate_equal_instance.name,
    )
    assert mocked_controller.forest.lookup.mock_calls[2] == mock.call(
        mocked_controller,
        requested_results[1],
        validate_equal_instance.name,
    )

  def test_apply__valid_lookups__performs_each_expected_b_lookup(
      self,
      mocked_controller: mock.Mock,
      validate_equal_instance: ValidateEqual,
  ) -> None:
    validate_equal_instance.apply(mocked_controller)

    requested_results = list(validate_equal_instance.saved_results_b)
    assert mocked_controller.forest.lookup.call_count == (
        len(requested_results) * 2
    )
    assert mocked_controller.forest.lookup.mock_calls[1] == mock.call(
        mocked_controller,
        requested_results[0],
        validate_equal_instance.name,
    )
    assert mocked_controller.forest.lookup.mock_calls[3] == mock.call(
        mocked_controller,
        requested_results[1],
        validate_equal_instance.name,
    )

  def test_apply__equal_lookup_results__does_not_raise_exception(
      self,
      mocked_controller: mock.Mock,
      validate_equal_instance: ValidateEqual,
  ) -> None:
    mocked_controller.forest.lookup.side_effect = (
        "result_0",
        "result_0",
        "result_1",
        "result_1",
    )

    validate_equal_instance.apply(mocked_controller)

  def test_apply__equal_lookup_results__outputs_expected_lookup_results(
      self,
      method_mocker: "AliasMethodMocker",
      mocked_controller: mock.Mock,
      mocked_result_sets: Dict[str, List[str]],
      validate_equal_instance: ValidateEqual,
  ) -> None:
    mocked_print = method_mocker(validate_equal_instance.print)
    mocked_controller.forest.lookup.side_effect = (
        "result_0",
        "result_0",
        "result_1",
        "result_1",
    )
    expected_mock_calls: List[str] = []
    for index, mock_result in enumerate(mocked_result_sets["a"]):
      expected_mock_calls.append(
          validate_equal_instance.msg_fmt_comparison_success.format(
              mock_result,
              mocked_result_sets["b"][index],
          )
      )

    validate_equal_instance.apply(mocked_controller)

    assert mocked_print.mock_calls == list(map(mock.call, expected_mock_calls))

  def test_apply__unequal_lookup_results__raises_exception(
      self,
      mocked_controller: mock.Mock,
      validate_equal_instance: ValidateEqual,
  ) -> None:
    mocked_controller.forest.lookup.side_effect = (
        "result_0",
        "result_1",
        "result_0",
        "result_1",
    )

    with pytest.raises(ValidationFailure) as exc:
      validate_equal_instance.apply(mocked_controller)

    assert_is_validation_failure(
        exc,
        description_t=(
            validate_equal_instance.msg_fmt_comparison_failure,
            list(validate_equal_instance.saved_results_a)[0].name,
            list(validate_equal_instance.saved_results_b)[0].name,
        ),
        detail_t=(
            validate_equal_instance.msg_fmt_comparison_failure,
            "result_0",
            "result_1",
        ),
        validator=validate_equal_instance,
    )
