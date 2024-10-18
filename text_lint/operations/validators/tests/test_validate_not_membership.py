"""Test the ValidateNotMembership class."""

from typing import Dict, List
from unittest import mock

import pytest
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
from text_lint.__helpers__.validators import (
    assert_is_invalid_comparison,
    assert_is_validation_failure,
)
from text_lint.exceptions.validators import (
    ValidationFailure,
    ValidationInvalidComparison,
)
from ..bases.validator_base import ValidatorBase
from ..validate_not_membership import (
    YAML_EXAMPLE,
    YAML_EXAMPLE_COMPONENTS,
    ValidateNotMembership,
)


class TestValidateNotMembership:
  """Test the ValidateNotMembership class."""

  def test_initialize__defined__attributes(
      self,
      validate_not_membership_instance: ValidateNotMembership,
      mocked_validator_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "validates non-membership of values inside other values",
        "internal_use_only": False,
        "name": mocked_validator_name,
        "operation": "validate_not_membership",
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(
        validate_not_membership_instance,
        attributes,
    )

  def test_initialize__translations(
      self,
      validate_not_membership_instance: ValidateNotMembership,
  ) -> None:
    assert_is_translated(validate_not_membership_instance.hint)
    assert_is_translated(
        validate_not_membership_instance.msg_fmt_comparison_failure
    )
    assert_is_translated(
        validate_not_membership_instance.msg_fmt_comparison_success
    )
    assert_is_translated(
        validate_not_membership_instance.msg_fmt_invalid_comparison_detail
    )

  def test_initialize__inheritance(
      self,
      validate_not_membership_instance: ValidateNotMembership,
  ) -> None:
    assert_operation_inheritance(
        validate_not_membership_instance,
        bases=(ValidatorBase, ValidateNotMembership),
    )
    assert_is_translated_yaml_example(
        validate_not_membership_instance.yaml_example,
        YAML_EXAMPLE_COMPONENTS,
    )

  @spy_on_validate_parameters(ValidateNotMembership)
  def test_initialize__parameter_validation(
      self,
      validate_parameters_spy: mock.Mock,
      validate_not_membership_instance: ValidateNotMembership,
      base_parameter_definitions: AliasParameterDefinitions,
  ) -> None:
    assert_parameter_schema(
        instance=validate_not_membership_instance,
        parameter_definitions=base_parameter_definitions,
    )
    validate_parameters_spy.assert_called_once_with(
        validate_not_membership_instance
    )

  @pytest.mark.usefixtures(
      "scenario__comparison__lookup_results_not_membership"
  )
  def test_apply__not_member_lookup_results__does_not_raise_exception(
      self,
      mocked_state: mock.Mock,
      validate_not_membership_instance: ValidateNotMembership,
  ) -> None:
    validate_not_membership_instance.apply(mocked_state)

  @pytest.mark.usefixtures(
      "scenario__comparison__lookup_results_not_membership"
  )
  def test_apply__not_member_lookup_results__logs_expected_lookup_results(
      self,
      mocked_state: mock.Mock,
      mocked_lookup_expression_sets: Dict[str, List[str]],
      validate_not_membership_instance: ValidateNotMembership,
  ) -> None:
    validate_not_membership_instance.apply(mocked_state)

    assert mocked_state.log.mock_calls == [
        mock.call(
            ValidateNotMembership.msg_fmt_comparison_success.format(
                mock_result,
                mocked_lookup_expression_sets["b"][index],
            ),
            indent=True,
        )
        for index, mock_result in enumerate(mocked_lookup_expression_sets["a"])
    ]

  @pytest.mark.usefixtures("scenario__comparison__lookup_results_membership")
  def test_apply__is_member_lookup_results__raises_exception(
      self,
      mocked_state: mock.Mock,
      validate_not_membership_instance: ValidateNotMembership,
  ) -> None:
    with pytest.raises(ValidationFailure) as exc:
      validate_not_membership_instance.apply(mocked_state)

    assert_is_validation_failure(
        exc,
        description_t=(
            validate_not_membership_instance.msg_fmt_comparison_failure,
            list(validate_not_membership_instance.lookup_expression_set_a
                )[0].name,
            list(validate_not_membership_instance.lookup_expression_set_b
                )[0].name,
        ),
        detail_t=(
            validate_not_membership_instance.msg_fmt_comparison_failure,
            "['result_0']",
            "result_0",
        ),
        validator=validate_not_membership_instance,
    )

  @pytest.mark.usefixtures(
      "scenario__comparison__lookup_results_invalid_membership"
  )
  def test_apply__invalid_membership_test__raises_exception(
      self,
      mocked_state: mock.Mock,
      validate_not_membership_instance: ValidateNotMembership,
  ) -> None:
    with pytest.raises(ValidationInvalidComparison) as exc:
      validate_not_membership_instance.apply(mocked_state)

    assert_is_invalid_comparison(
        exc,
        description_t=(
            validate_not_membership_instance.
            msg_fmt_invalid_comparison_description,
            list(validate_not_membership_instance.lookup_expression_set_a
                )[0].name,
            list(validate_not_membership_instance.lookup_expression_set_b
                )[0].name,
        ),
        detail_t=(
            validate_not_membership_instance.msg_fmt_invalid_comparison_detail,
            str(type("result_0")),
            str(type(['result_1'])),
        ),
        validator=validate_not_membership_instance,
    )
