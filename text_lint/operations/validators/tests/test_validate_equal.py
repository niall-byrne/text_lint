"""Test the ValidateEqual class."""

from typing import Dict, List
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
from ..bases.validator_base import ValidatorBase
from ..validate_equal import YAML_EXAMPLE, ValidateEqual


class TestValidateEqual:
  """Test the ValidateEqual class."""

  def test_initialize__defined__attributes(
      self,
      validate_equal_instance: ValidateEqual,
      mocked_validator_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "validates equality between sets of values",
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
        bases=(ValidatorBase, ValidateEqual),
    )

  @pytest.mark.usefixtures("scenario__comparison__lookup_results_equal")
  def test_apply__equal_lookup_results__does_not_raise_exception(
      self,
      mocked_state: mock.Mock,
      validate_equal_instance: ValidateEqual,
  ) -> None:
    validate_equal_instance.apply(mocked_state)

  @pytest.mark.usefixtures("scenario__comparison__lookup_results_equal")
  def test_apply__equal_lookup_results__logs_expected_lookup_results(
      self,
      mocked_state: mock.Mock,
      mocked_lookup_expression_sets: Dict[str, List[str]],
      validate_equal_instance: ValidateEqual,
  ) -> None:
    validate_equal_instance.apply(mocked_state)

    assert mocked_state.log.mock_calls == [
        mock.call(
            ValidateEqual.msg_fmt_comparison_success.format(
                mock_result,
                mocked_lookup_expression_sets["b"][index],
            ),
            indent=True,
        )
        for index, mock_result in enumerate(mocked_lookup_expression_sets["a"])
    ]

  @pytest.mark.usefixtures("scenario__comparison__lookup_results_not_equal")
  def test_apply__not_equal_lookup_results__raises_exception(
      self,
      mocked_state: mock.Mock,
      validate_equal_instance: ValidateEqual,
  ) -> None:
    with pytest.raises(ValidationFailure) as exc:
      validate_equal_instance.apply(mocked_state)

    assert_is_validation_failure(
        exc,
        description_t=(
            validate_equal_instance.msg_fmt_comparison_failure,
            list(validate_equal_instance.lookup_expression_set_a)[0].name,
            list(validate_equal_instance.lookup_expression_set_b)[0].name,
        ),
        detail_t=(
            validate_equal_instance.msg_fmt_comparison_failure,
            "result_0",
            "result_1",
        ),
        validator=validate_equal_instance,
    )
