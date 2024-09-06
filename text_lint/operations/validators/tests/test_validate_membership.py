"""Test the ValidateMembership class."""

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
from ..validate_membership import YAML_EXAMPLE, ValidateMembership


class TestValidateMembership:
  """Test the ValidateMembership class."""

  def test_initialize__defined__attributes(
      self,
      validate_membership_instance: ValidateMembership,
      mocked_validator_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "validates membership of values inside other values",
        "internal_use_only": False,
        "name": mocked_validator_name,
        "operation": "validate_membership",
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(
        validate_membership_instance,
        attributes,
    )

  def test_initialize__translations(
      self,
      validate_membership_instance: ValidateMembership,
  ) -> None:
    assert_is_translated(validate_membership_instance.hint)
    assert_is_translated(
        validate_membership_instance.msg_fmt_comparison_failure
    )
    assert_is_translated(
        validate_membership_instance.msg_fmt_comparison_success
    )

  def test_initialize__inheritance(
      self,
      validate_membership_instance: ValidateMembership,
  ) -> None:
    assert_operation_inheritance(
        validate_membership_instance,
        bases=(ValidatorBase, ValidateMembership),
    )

  @pytest.mark.usefixtures("scenario__comparison__lookup_results_membership")
  def test_apply__is_member_lookup_results__does_not_raise_exception(
      self,
      mocked_state: mock.Mock,
      validate_membership_instance: ValidateMembership,
  ) -> None:
    validate_membership_instance.apply(mocked_state)

  @pytest.mark.usefixtures("scenario__comparison__lookup_results_membership")
  def test_apply__is_member_lookup_results__logs_expected_lookup_results(
      self,
      mocked_state: mock.Mock,
      mocked_lookup_expression_sets: Dict[str, List[str]],
      validate_membership_instance: ValidateMembership,
  ) -> None:
    validate_membership_instance.apply(mocked_state)

    assert mocked_state.log.mock_calls == [
        mock.call(
            ValidateMembership.msg_fmt_comparison_success.format(
                mock_result,
                mocked_lookup_expression_sets["b"][index],
            ),
            indent=True,
        )
        for index, mock_result in enumerate(mocked_lookup_expression_sets["a"])
    ]

  @pytest.mark.usefixtures(
      "scenario__comparison__lookup_results_not_membership"
  )
  def test_apply__not_member_lookup_results__raises_exception(
      self,
      mocked_state: mock.Mock,
      validate_membership_instance: ValidateMembership,
  ) -> None:
    with pytest.raises(ValidationFailure) as exc:
      validate_membership_instance.apply(mocked_state)

    assert_is_validation_failure(
        exc,
        description_t=(
            validate_membership_instance.msg_fmt_comparison_failure,
            list(validate_membership_instance.lookup_expression_set_a)[0].name,
            list(validate_membership_instance.lookup_expression_set_b)[0].name,
        ),
        detail_t=(
            validate_membership_instance.msg_fmt_comparison_failure,
            "['result_0']",
            "result_1",
        ),
        validator=validate_membership_instance,
    )

  @pytest.mark.usefixtures(
      "scenario__comparison__lookup_results_invalid_membership"
  )
  def test_apply__invalid_membership_test__raises_exception(
      self,
      mocked_state: mock.Mock,
      validate_membership_instance: ValidateMembership,
  ) -> None:
    with pytest.raises(ValidationFailure) as exc:
      validate_membership_instance.apply(mocked_state)

    assert_is_validation_failure(
        exc,
        description_t=(
            validate_membership_instance.msg_fmt_comparison_failure,
            list(validate_membership_instance.lookup_expression_set_a)[0].name,
            list(validate_membership_instance.lookup_expression_set_b)[0].name,
        ),
        detail_t=(
            validate_membership_instance.msg_fmt_comparison_failure,
            "result_0",
            "['result_1']",
        ),
        validator=validate_membership_instance,
    )
