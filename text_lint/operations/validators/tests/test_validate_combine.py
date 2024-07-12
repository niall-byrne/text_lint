"""Test the ValidateCombine class."""

from typing import TYPE_CHECKING, List
from unittest import mock

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.operations.validators.args.result_set import ResultSetArg
from text_lint.results.tree import ResultTree
from ..bases.validator_base import ValidationBase
from ..validate_combine import YAML_EXAMPLE, ValidateCombine

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.__fixtures__.mocks import AliasMethodMocker


class TestValidateCombine:
  """Test the ValidateCombine class."""

  def test_initialize__defined__attributes(
      self,
      mocked_validator_name: str,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "combines a set of lookups into a new saved result",
        "internal_use_only": False,
        "name": mocked_validator_name,
        "operation": "validate_combine",
        "yaml_example": YAML_EXAMPLE,
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
        bases=(ValidationBase, ValidateCombine),
    )

  def test_initialize__creates_result_set_arg_instance(
      self,
      mocked_result_set_a: List[str],
      validate_combine_instance: ValidateCombine,
  ) -> None:
    assert isinstance(validate_combine_instance.saved_results, ResultSetArg)

    requested_results = list(validate_combine_instance.saved_results)
    assert requested_results[0].name == mocked_result_set_a[0]
    assert requested_results[1].name == mocked_result_set_a[1]

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
      mocked_controller: mock.Mock,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_controller.forest.lookup.side_effect = (
        "result_0",
        "result_1",
    )

    validate_combine_instance.apply(mocked_controller)

    requested_results = list(validate_combine_instance.saved_results)
    assert mocked_controller.forest.lookup.call_count == (
        len(requested_results)
    )
    assert mocked_controller.forest.lookup.mock_calls[0] == mock.call(
        mocked_controller,
        requested_results[0],
        validate_combine_instance.name,
    )
    assert mocked_controller.forest.lookup.mock_calls[1] == mock.call(
        mocked_controller,
        requested_results[1],
        validate_combine_instance.name,
    )

  def test_apply__str_results__creates_expected_result_tree_children(
      self,
      mocked_combined_result_tree_name: str,
      mocked_controller: mock.Mock,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_controller.forest.lookup.side_effect = (
        "result_0",
        "result_1",
    )

    validate_combine_instance.apply(mocked_controller)

    assert isinstance(validate_combine_instance.new_tree, ResultTree)
    assert validate_combine_instance.new_tree.value == \
        mocked_combined_result_tree_name
    for index, child in enumerate(validate_combine_instance.new_tree.children):
      assert isinstance(child, ResultTree)
      assert child.value == "result_{0}".format(index)

  def test_apply__list_results__creates_expected_result_tree_children(
      self,
      mocked_combined_result_tree_name: str,
      mocked_controller: mock.Mock,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_controller.forest.lookup.side_effect = (
        "result_0",
        ["result_1"],
    )

    validate_combine_instance.apply(mocked_controller)

    assert isinstance(validate_combine_instance.new_tree, ResultTree)
    assert validate_combine_instance.new_tree.value == \
        mocked_combined_result_tree_name
    for index, child in enumerate(validate_combine_instance.new_tree.children):
      assert isinstance(child, ResultTree)
      assert child.value == "result_{0}".format(index)

  def test_apply__grouped_results__creates_expected_result_tree_children(
      self,
      mocked_combined_result_tree_name: str,
      mocked_controller: mock.Mock,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_controller.forest.lookup.side_effect = (
        [
            ["result_0"],
            ["result_1", "result_2"],
        ]
    )

    validate_combine_instance.apply(mocked_controller)

    assert isinstance(validate_combine_instance.new_tree, ResultTree)
    assert validate_combine_instance.new_tree.value == \
        mocked_combined_result_tree_name
    for index, child in enumerate(validate_combine_instance.new_tree.children):
      assert isinstance(child, ResultTree)
      assert child.value == "result_{0}".format(index)

  def test_apply__valid_results__adds_new_result_tree_to_forest(
      self,
      mocked_controller: mock.Mock,
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_controller.forest.lookup.side_effect = (
        "result_0",
        "result_1",
    )

    validate_combine_instance.apply(mocked_controller)

    mocked_controller.forest.add.assert_called_once_with(
        validate_combine_instance.new_tree
    )

  def test_apply__valid_results__outputs_expected_lookup_results(
      self,
      method_mocker: "AliasMethodMocker",
      mocked_controller: mock.Mock,
      mocked_result_set_a: List[str],
      validate_combine_instance: ValidateCombine,
  ) -> None:
    mocked_controller.forest.lookup.side_effect = (
        "result_0",
        "result_1",
    )
    mocked_print = method_mocker(validate_combine_instance.print)
    expected_mock_calls: List[str] = []
    for result in mocked_result_set_a:
      expected_mock_calls.append(
          validate_combine_instance.msg_fmt_combine.format(
              result,
              validate_combine_instance.new_tree.value,
          )
      )

    validate_combine_instance.apply(mocked_controller)

    assert mocked_print.mock_calls == list(map(mock.call, expected_mock_calls))
