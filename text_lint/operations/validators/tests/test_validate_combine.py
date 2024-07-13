"""Test the ValidateCombine class."""

from typing import List
from unittest import mock

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.operations.validators.args.lookup_expression import (
    LookupExpressionSetArg,
)
from text_lint.results.tree import ResultTree
from ..bases.validator_base import ValidatorBase
from ..validate_combine import ValidateCombine


class TestValidateCombine:
  """Test the ValidateCombine class."""

  def test_initialize__defined__attributes(
      self,
      mocked_validator_name: str,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "combines a set of lookups into a new save id",
        "name": mocked_validator_name,
        "operation": "validate_combine",
    }

    assert_operation_attributes(
        validate_combine_instance,
        attributes,
    )

  def test_initialize__translations(
      self,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    assert_is_translated(validate_combine_instance.hint)
    assert_is_translated(validate_combine_instance.msg_fmt_combine)

  def test_initialize__inheritance(
      self,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    assert_operation_inheritance(
        validate_combine_instance,
        bases=(ValidatorBase, ValidateCombine),
    )

  def test_initialize__creates_result_set_arg_instance(
      self,
      mocked_lookup_expression_set_a: List[str],
      validate_combine_instance: ValidateCombine,
  ) -> None:
    assert isinstance(
        validate_combine_instance.saved_results,
        LookupExpressionSetArg,
    )

    requested_results = list(validate_combine_instance.saved_results)
    assert requested_results[0].name == mocked_lookup_expression_set_a[0]
    assert requested_results[1].name == mocked_lookup_expression_set_a[1]

  def test_initialize__creates_empty_result_tree_instance(
      self,
      mocked_combined_result_tree_name: str,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    assert isinstance(validate_combine_instance.new_tree, ResultTree)
    assert validate_combine_instance.new_tree.value == \
        mocked_combined_result_tree_name
    assert len(validate_combine_instance.new_tree.children) == 0

  def test_apply__performs_each_expected_lookup(
      self,
      mocked_state: mock.Mock,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_state.lookup_expression.side_effect = (
        "result_0",
        "result_1",
    )

    validate_combine_instance.apply(mocked_state)

    requested_results = list(validate_combine_instance.saved_results)
    assert mocked_state.lookup_expression.call_count == (len(requested_results))
    assert mocked_state.lookup_expression.mock_calls[0] == mock.call(
        requested_results[0],
    )
    assert mocked_state.lookup_expression.mock_calls[1] == mock.call(
        requested_results[1],
    )

  def test_apply__str_results__creates_expected_result_tree_children(
      self,
      mocked_combined_result_tree_name: str,
      mocked_state: mock.Mock,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_state.lookup_expression.side_effect = (
        "result_0",
        "result_1",
    )

    validate_combine_instance.apply(mocked_state)

    assert isinstance(validate_combine_instance.new_tree, ResultTree)
    assert validate_combine_instance.new_tree.value == \
        mocked_combined_result_tree_name
    for index, child in enumerate(validate_combine_instance.new_tree.children):
      assert isinstance(child, ResultTree)
      assert child.value == "result_{0}".format(index)

  def test_apply__list_results__creates_expected_result_tree_children(
      self,
      mocked_combined_result_tree_name: str,
      mocked_state: mock.Mock,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_state.lookup_expression.side_effect = (
        "result_0",
        ["result_1"],
    )

    validate_combine_instance.apply(mocked_state)

    assert isinstance(validate_combine_instance.new_tree, ResultTree)
    assert validate_combine_instance.new_tree.value == \
        mocked_combined_result_tree_name
    for index, child in enumerate(validate_combine_instance.new_tree.children):
      assert isinstance(child, ResultTree)
      assert child.value == "result_{0}".format(index)

  def test_apply__grouped_results__creates_expected_result_tree_children(
      self,
      mocked_combined_result_tree_name: str,
      mocked_state: mock.Mock,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_state.lookup_expression.side_effect = (
        [
            ["result_0"],
            ["result_1", "result_2"],
        ]
    )

    validate_combine_instance.apply(mocked_state)

    assert isinstance(validate_combine_instance.new_tree, ResultTree)
    assert validate_combine_instance.new_tree.value == \
        mocked_combined_result_tree_name
    for index, child in enumerate(validate_combine_instance.new_tree.children):
      assert isinstance(child, ResultTree)
      assert child.value == "result_{0}".format(index)

  def test_apply__valid_results__adds_new_result_tree_to_forest(
      self,
      mocked_state: mock.Mock,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_state.lookup_expression.side_effect = (
        "result_0",
        "result_1",
    )

    validate_combine_instance.apply(mocked_state)

    mocked_state.save.assert_called_once_with(
        validate_combine_instance.new_tree
    )

  def test_apply__valid_results__logs_expected_lookup_results(
      self,
      mocked_state: mock.Mock,
      mocked_lookup_expression_set_a: List[str],
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_state.lookup_expression.side_effect = (
        "result_0",
        "result_1",
    )

    validate_combine_instance.apply(mocked_state)

    assert mocked_state.log.mock_calls == [
        mock.call(
            ValidateCombine.msg_fmt_combine.format(
                mock_result,
                validate_combine_instance.new_tree.value,
            ),
            indent=True,
        ) for mock_result in mocked_lookup_expression_set_a
    ]
