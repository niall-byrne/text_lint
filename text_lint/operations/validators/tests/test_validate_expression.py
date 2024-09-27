"""Test the ValidateExpression class."""

from typing import Any, List, Tuple
from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import (
    assert_is_translated,
    assert_is_translated_yaml_example,
)
from text_lint.__helpers__.validators import (
    assert_is_invalid_comparison,
    assert_is_validation_failure,
    validate_expression_with_numeric_lookup_results,
)
from text_lint.exceptions.schema import ValidatorParametersInvalid
from text_lint.exceptions.validators import (
    ValidationFailure,
    ValidationInvalidComparison,
)
from text_lint.operations.validators.args.lookup_expression import (
    LookupExpressionSetArg,
)
from text_lint.operations.validators.expressions import expressions_registry
from text_lint.results.tree import ResultTree
from ..bases.validator_base import ValidatorBase
from ..validate_expression import (
    YAML_EXAMPLE,
    YAML_EXAMPLE_COMPONENTS,
    ValidateExpression,
)


class TestValidateExpression:
  """Test the ValidateExpression class."""

  @pytest.mark.parametrize("validate_expression_instance", ["+"], indirect=True)
  def test_initialize__defined__attributes(
      self,
      mocked_validator_name: str,
      validate_expression_instance: ValidateExpression,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "perform math on save ids to create a new save id",
        "internal_use_only": False,
        "name": mocked_validator_name,
        "operation": "validate_expression",
        "operator": "+",
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(
        validate_expression_instance,
        attributes,
    )

  @pytest.mark.parametrize("validate_expression_instance", ["+"], indirect=True)
  def test_initialize__translations(
      self,
      validate_expression_instance: ValidateExpression,
  ) -> None:
    assert_is_translated(validate_expression_instance.hint)
    assert_is_translated(ValidateExpression.msg_fmt_comparison_failure)
    assert_is_translated(ValidateExpression.msg_fmt_comparison_success)
    assert_is_translated(
        ValidateExpression.msg_fmt_invalid_comparison_description
    )
    assert_is_translated(
        validate_expression_instance.msg_fmt_invalid_comparison_detail
    )
    assert_is_translated(ValidateExpression.msg_fmt_invalid_operator)
    assert_is_translated_yaml_example(
        validate_expression_instance.yaml_example,
        YAML_EXAMPLE_COMPONENTS,
        notes=True,
    )
    assert validate_expression_instance.msg_fmt_comparison_failure == (
        ValidateExpression.msg_fmt_comparison_failure.replace(
            "{2}",
            validate_expression_instance.operator,
        )
    )
    assert validate_expression_instance.msg_fmt_comparison_success == (
        ValidateExpression.msg_fmt_comparison_success.replace(
            "{2}",
            validate_expression_instance.operator,
        )
    )
    assert validate_expression_instance.\
        msg_fmt_invalid_comparison_description == (
            ValidateExpression.msg_fmt_invalid_comparison_description.replace(
                "{2}",
                validate_expression_instance.operator,
            )
        )

  @pytest.mark.parametrize("validate_expression_instance", ["+"], indirect=True)
  def test_initialize__inheritance(
      self,
      validate_expression_instance: ValidateExpression,
  ) -> None:
    assert_operation_inheritance(
        validate_expression_instance,
        bases=(ValidatorBase, ValidateExpression),
    )

  @pytest.mark.parametrize("validate_expression_instance", ["+"], indirect=True)
  def test_initialize__creates_result_set_arg_a_instance(
      self,
      mocked_lookup_expression_set_a: List[str],
      validate_expression_instance: ValidateExpression,
  ) -> None:
    assert isinstance(
        validate_expression_instance.lookup_expression_set_a,
        LookupExpressionSetArg,
    )

    requested_results = list(
        validate_expression_instance.lookup_expression_set_a
    )
    assert requested_results[0].name == mocked_lookup_expression_set_a[0]
    assert requested_results[1].name == mocked_lookup_expression_set_a[1]

  @pytest.mark.parametrize("validate_expression_instance", ["+"], indirect=True)
  def test_initialize__creates_result_set_arg_b_instance(
      self,
      mocked_lookup_expression_set_b: List[str],
      validate_expression_instance: ValidateExpression,
  ) -> None:
    assert isinstance(
        validate_expression_instance.lookup_expression_set_b,
        LookupExpressionSetArg,
    )

    requested_results = list(
        validate_expression_instance.lookup_expression_set_b
    )
    assert requested_results[0].name == mocked_lookup_expression_set_b[0]
    assert requested_results[1].name == mocked_lookup_expression_set_b[1]

  @pytest.mark.parametrize("validate_expression_instance", ["+"], indirect=True)
  def test_initialize__creates_empty_result_tree_instance(
      self,
      mocked_result_tree_name: str,
      validate_expression_instance: ValidateExpression,
  ) -> None:
    assert isinstance(validate_expression_instance.new_tree, ResultTree)
    assert validate_expression_instance.new_tree.value == \
        mocked_result_tree_name
    assert len(validate_expression_instance.new_tree.children) == 0

  @pytest.mark.parametrize("invalid_operator", ["!", "@"])
  def test_initialize__invalid_operator__raises_exception(
      self,
      mocked_lookup_expression_set_a: List[str],
      mocked_lookup_expression_set_b: List[str],
      mocked_result_tree_name: str,
      mocked_validator_name: str,
      invalid_operator: str,
  ) -> None:
    with pytest.raises(ValidatorParametersInvalid) as exc:
      ValidateExpression(
          mocked_validator_name,
          operator=invalid_operator,
          new_saved=mocked_result_tree_name,
          saved_a=mocked_lookup_expression_set_a,
          saved_b=mocked_lookup_expression_set_b,
      )

    assert str(exc.value) == \
        ValidateExpression.msg_fmt_invalid_operator.format(invalid_operator)

  @validate_expression_with_numeric_lookup_results
  @pytest.mark.parametrize("validate_expression_instance", ["+"], indirect=True)
  def test_apply__valid_lookups__performs_each_expected_a_lookup(
      self,
      mocked_state: mock.Mock,
      validate_expression_instance: ValidateExpression,
      lookup_results: int,
  ) -> None:
    mocked_state.lookup_expression.side_effect = lookup_results

    validate_expression_instance.apply(mocked_state)

    extracted_results = list(
        validate_expression_instance.lookup_expression_set_a
    )
    assert mocked_state.lookup_expression.call_count == (
        len(extracted_results) * 2
    )
    assert mocked_state.lookup_expression.mock_calls[0] == mock.call(
        extracted_results[0],
    )
    assert mocked_state.lookup_expression.mock_calls[2] == mock.call(
        extracted_results[1],
    )

  @validate_expression_with_numeric_lookup_results
  @pytest.mark.parametrize("validate_expression_instance", ["+"], indirect=True)
  def test_apply__valid_lookups__performs_each_expected_b_lookup(
      self,
      mocked_state: mock.Mock,
      validate_expression_instance: ValidateExpression,
      lookup_results: int,
  ) -> None:
    mocked_state.lookup_expression.side_effect = lookup_results

    validate_expression_instance.apply(mocked_state)

    extracted_results = list(
        validate_expression_instance.lookup_expression_set_b
    )
    assert mocked_state.lookup_expression.call_count == (
        len(extracted_results) * 2
    )
    assert mocked_state.lookup_expression.mock_calls[1] == mock.call(
        extracted_results[0],
    )
    assert mocked_state.lookup_expression.mock_calls[3] == mock.call(
        extracted_results[1],
    )

  @validate_expression_with_numeric_lookup_results
  @pytest.mark.parametrize(
      "validate_expression_instance",
      expressions_registry.keys(),
      indirect=True,
  )
  def test_apply__vary_operator__creates_expected_result_tree_children(
      self,
      mocked_result_tree_name: str,
      mocked_state: mock.Mock,
      validate_expression_instance: ValidateExpression,
      lookup_results: int,
  ) -> None:
    mocked_state.lookup_expression.side_effect = lookup_results

    try:
      validate_expression_instance.apply(mocked_state)
    except ValidationFailure:
      pass

    assert isinstance(validate_expression_instance.new_tree, ResultTree)
    assert validate_expression_instance.new_tree.value == \
        mocked_result_tree_name
    for child, index in zip(
        validate_expression_instance.new_tree.children,
        [1.0, 3.0],
    ):
      expression_class = expressions_registry[
          validate_expression_instance.operator]
      assert isinstance(child, ResultTree)
      assert child.value == str(expression_class().apply(index, index + 1))

  @pytest.mark.parametrize(
      "validate_expression_instance,lookup_results",
      [
          ["+", (1, 2, 3, 4)],
          ["-", (1, 2, 3, 4)],
          ["*", (1, 2, 3, 4)],
          ["/", (1, 2, 3, 4)],
          ["^", (1, 2, 3, 4)],
          ["<", (1, 2, 1, 2)],
          ["<=", (1, 2, 1, 2)],
          [">", (2, 1, 2, 1)],
          [">=", (2, 1, 2, 1)],
      ],
      indirect=["validate_expression_instance"],
      ids=str,
  )
  def test_apply__vary_operator__when_successful__adds_tree_to_forest(
      self,
      mocked_state: mock.Mock,
      validate_expression_instance: ValidateExpression,
      lookup_results: int,
  ) -> None:
    mocked_state.lookup_expression.side_effect = lookup_results

    validate_expression_instance.apply(mocked_state)

    mocked_state.save.assert_called_once_with(
        validate_expression_instance.new_tree
    )

  @pytest.mark.parametrize(
      "validate_expression_instance,lookup_results",
      [
          ["<", (2, 1, 2, 1)],
          ["<=", (2, 1, 2, 1)],
          [">", (1, 2, 1, 2)],
          [">=", (1, 2, 1, 2)],
      ],
      indirect=["validate_expression_instance"],
      ids=str,
  )
  def test_apply__vary_operator__when_failure__does_not_add_results(
      self,
      mocked_state: mock.Mock,
      validate_expression_instance: ValidateExpression,
      lookup_results: Tuple[int, int, int, int],
  ) -> None:
    mocked_state.lookup_expression.side_effect = lookup_results

    with pytest.raises(ValidationFailure):
      validate_expression_instance.apply(mocked_state)

    mocked_state.forest.add.assert_not_called()

  @pytest.mark.parametrize(
      "validate_expression_instance,lookup_results",
      [
          ["<", (2, 1, 2, 1)],
          ["<=", (2, 1, 2, 1)],
          [">", (1, 2, 1, 2)],
          [">=", (1, 2, 1, 2)],
      ],
      indirect=["validate_expression_instance"],
      ids=str,
  )
  def test_apply__vary_operator__when_failure__raises_correct_exception(
      self,
      mocked_state: mock.Mock,
      mocked_lookup_expression_set_a: List[str],
      mocked_lookup_expression_set_b: List[str],
      validate_expression_instance: ValidateExpression,
      lookup_results: Tuple[int, int, int, int],
  ) -> None:
    mocked_state.lookup_expression.side_effect = lookup_results

    with pytest.raises(ValidationFailure) as exc:
      validate_expression_instance.apply(mocked_state)

    assert_is_validation_failure(
        exc=exc,
        description_t=(
            ValidateExpression.msg_fmt_comparison_failure,
            mocked_lookup_expression_set_a[0],
            mocked_lookup_expression_set_b[0],
            validate_expression_instance.operator,
        ),
        detail_t=(
            ValidateExpression.msg_fmt_comparison_failure,
            lookup_results[0],
            lookup_results[1],
            validate_expression_instance.operator,
        ),
        validator=validate_expression_instance
    )

  @pytest.mark.parametrize(
      "validate_expression_instance,lookup_results",
      [
          ["+", ([], ())],
          ["-", ("a", "b")],
          ["/", ({}, "")],
      ],
      indirect=["validate_expression_instance"],
      ids=str,
  )
  def test_apply__valid_lookups__non_float_values__raise_exception(
      self,
      mocked_state: mock.Mock,
      mocked_lookup_expression_set_a: List[str],
      mocked_lookup_expression_set_b: List[str],
      validate_expression_instance: ValidateExpression,
      lookup_results: Any,
  ) -> None:
    mocked_state.lookup_expression.side_effect = lookup_results

    with pytest.raises(ValidationInvalidComparison) as exc:
      validate_expression_instance.apply(mocked_state)

    assert_is_invalid_comparison(
        exc=exc,
        description_t=(
            ValidateExpression.msg_fmt_invalid_comparison_description,
            mocked_lookup_expression_set_a[0],
            mocked_lookup_expression_set_b[0],
            validate_expression_instance.operator,
        ),
        detail_t=(
            ValidateExpression.msg_fmt_invalid_comparison_detail,
            str(type(lookup_results[0])),
            str(type(lookup_results[1])),
            validate_expression_instance.operator,
        ),
        validator=validate_expression_instance
    )
