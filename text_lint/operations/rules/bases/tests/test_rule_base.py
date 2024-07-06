"""Test the RuleBase class."""

from typing import Type
from unittest import mock

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.rules import assert_rule_attributes
from text_lint.operations.rules.bases.rule_base import RuleBase


class TestRuleBase:
  """Test the RuleBase class."""

  def test_intialize__defaults__attributes(
      self,
      concrete_rule_base_class: Type[RuleBase],
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "a concrete hint",
        "matches": [],
        "name": "concrete name",
        "operation": concrete_rule_base_class.operation,
        "save": None,
        "splits": {},
        "yaml_example": "mocked_yaml_example_rule",
    }

    instance = concrete_rule_base_class(name="concrete name",)

    assert_rule_attributes(instance, attributes)

  def test_initialize__defined__attributes(
      self,
      concrete_rule_base_instance: RuleBase,
      concrete_rule_base_class: Type[RuleBase],
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "a concrete hint",
        "matches": [],
        "name": "concrete name",
        "operation": concrete_rule_base_class.operation,
        "save": "save_id",
        "splits": {
            1: None
        },
        "yaml_example": "mocked_yaml_example_rule",
    }

    assert_rule_attributes(concrete_rule_base_instance, attributes)

  def test_initialize__inheritance(
      self,
      concrete_rule_base_instance: RuleBase,
  ) -> None:
    assert_operation_inheritance(concrete_rule_base_instance, bases=(RuleBase,))

  def test_apply__calls_mocked_implementation(
      self,
      concrete_rule_base_instance: RuleBase,
      mocked_implementation: mock.Mock,
  ) -> None:
    mocked_controller = mock.Mock()

    concrete_rule_base_instance.apply(mocked_controller)

    mocked_implementation.assert_called_once_with(mocked_controller)

  def test_results__no_save_group__returns_none(
      self,
      concrete_rule_base_instance: RuleBase,
  ) -> None:
    concrete_rule_base_instance.save = None

    assert concrete_rule_base_instance.results is None

  def test_results__with_save_group__creates_result_instance(
      self,
      concrete_rule_base_instance: RuleBase,
      mocked_result_class: mock.Mock,
  ) -> None:
    mocked_results = [mock.Mock(), mock.Mock()]
    expected_add_matches_calls = [
        mock.call(result.groups.return_value, {1: None})
        for result in mocked_results
    ]
    concrete_rule_base_instance.save = "save_group"
    setattr(concrete_rule_base_instance, "matches", mocked_results)

    _ = concrete_rule_base_instance.results

    mocked_result_class.assert_called_once_with("save_group")
    assert mocked_result_class.return_value.add_matches.mock_calls == (
        expected_add_matches_calls
    )

  def test_results__with_save_group__returns_result_instance(
      self,
      concrete_rule_base_instance: RuleBase,
      mocked_result_class: mock.Mock,
  ) -> None:
    concrete_rule_base_instance.save = "save_group"

    results = concrete_rule_base_instance.results

    assert results == mocked_result_class.return_value

  def test_schema_validator__is_a_noop(
      self,
      concrete_rule_base_instance: RuleBase,
  ) -> None:
    operation_instances = [concrete_rule_base_instance]
    mocked_yaml_definitions = [{"mock": "yaml"}]
    mocked_schema = mock.Mock()

    concrete_rule_base_instance.schema_validator(
        0,
        operation_instances,
        mocked_yaml_definitions,
        mocked_schema,
    )
