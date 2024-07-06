"""Test the AssertionBase class."""

from typing import List, Type
from unittest import mock

import pytest
from text_lint.__helpers__.assertion import (
    assert_assertion_attributes,
    assert_is_assertion_capture_group_not_found,
)
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.exceptions.assertions import AssertionCaptureGroupNotFound
from text_lint.exceptions.results import SplitGroupNotFound
from text_lint.operations.assertions.bases.assertion_base import AssertionBase


class TestAssertionBase:
  """Test the AssertionBase class."""

  def test_intialize__defaults__attributes(
      self,
      concrete_assertion_base_class: Type[AssertionBase],
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "a concrete hint",
        "name": "concrete name",
        "operation": concrete_assertion_base_class.operation,
        "save": None,
        "splits": {},
        "yaml_example": "mocked_yaml_example_assertion",
    }

    instance = concrete_assertion_base_class(name="concrete name",)

    assert_assertion_attributes(instance, attributes)

  def test_initialize__defined__attributes(
      self,
      concrete_assertion_base_instance: AssertionBase,
      concrete_assertion_base_class: Type[AssertionBase],
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "a concrete hint",
        "name": "concrete name",
        "operation": concrete_assertion_base_class.operation,
        "save": "save_id",
        "splits": {
            1: None
        },
        "yaml_example": "mocked_yaml_example_assertion",
    }

    assert_assertion_attributes(concrete_assertion_base_instance, attributes)

  def test_initialize__inheritance(
      self,
      concrete_assertion_base_instance: AssertionBase,
  ) -> None:
    assert_operation_inheritance(
        concrete_assertion_base_instance, bases=(AssertionBase,)
    )

  def test_apply__calls_mocked_implementation(
      self,
      concrete_assertion_base_instance: AssertionBase,
      mocked_implementation: mock.Mock,
  ) -> None:
    mocked_linter = mock.Mock()

    concrete_assertion_base_instance.apply(mocked_linter)

    mocked_implementation.assert_called_once_with(mocked_linter)

  def test_create_result_tree__no_save_group__returns_none(
      self,
      concrete_assertion_base_instance: AssertionBase,
  ) -> None:
    concrete_assertion_base_instance.save = None

    assert concrete_assertion_base_instance.\
        create_result_tree([mock.Mock()]) is None

  def test_create_result_tree__with_save_group__creates_result_instance(
      self,
      concrete_assertion_base_instance: AssertionBase,
      mocked_results: List[mock.Mock],
      mocked_result_class: mock.Mock,
  ) -> None:
    expected_add_matches_calls = [
        mock.call(result.groups.return_value, {1: None})
        for result in mocked_results
    ]
    concrete_assertion_base_instance.save = "save_group"

    _ = concrete_assertion_base_instance.create_result_tree(mocked_results)

    mocked_result_class.assert_called_once_with("save_group")
    assert mocked_result_class.return_value.add_matches.mock_calls == (
        expected_add_matches_calls
    )

  def test_create_result_tree__with_save_group__returns_result_instance(
      self,
      concrete_assertion_base_instance: AssertionBase,
      mocked_results: List[mock.Mock],
      mocked_result_class: mock.Mock,
  ) -> None:
    concrete_assertion_base_instance.save = "save_group"

    results = concrete_assertion_base_instance.create_result_tree(
        mocked_results
    )

    assert results == mocked_result_class.return_value

  def test_create_result_tree__invalid_capture_group__raises_exception(
      self,
      concrete_assertion_base_instance: AssertionBase,
      mocked_results: List[mock.Mock],
      mocked_result_class: mock.Mock,
  ) -> None:
    mocked_result_class.return_value.add_matches.side_effect = \
        SplitGroupNotFound(1)

    with pytest.raises(AssertionCaptureGroupNotFound) as exc:
      _ = concrete_assertion_base_instance.create_result_tree(mocked_results)

    assert_is_assertion_capture_group_not_found(
        exc=exc,
        assertion=concrete_assertion_base_instance,
        capture_group=1,
    )

  def test_schema_validator__is_a_noop(
      self,
      concrete_assertion_base_instance: AssertionBase,
  ) -> None:
    operation_instances = [concrete_assertion_base_instance]
    mocked_yaml_definitions = [{"mock": "yaml"}]
    mocked_schema = mock.Mock()

    concrete_assertion_base_instance.schema_validator(
        0,
        operation_instances,
        mocked_yaml_definitions,
        mocked_schema,
    )
