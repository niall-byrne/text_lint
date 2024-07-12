"""Test the RuleRegexBase class."""

from typing import Type

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.rules import assert_rule_attributes
from text_lint.operations.rules.bases.rule_base import RuleBase
from text_lint.operations.rules.bases.rule_regex_base import RuleRegexBase


class TestRuleRegexBase:
  """Test the RuleRegexBase class."""

  def test_intialize__defaults__attributes(
      self,
      concrete_rule_regex_base_class: Type[RuleRegexBase],
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "a concrete regex hint",
        "internal_use_only": False,
        "matches": [],
        "name": "concrete name",
        "operation": concrete_rule_regex_base_class.operation,
        "regex": r'(.*).py',
        "save": None,
        "splits": {},
        "yaml_example": "mocked_yaml_example_rule_regex",
    }

    instance = concrete_rule_regex_base_class(
        name="concrete name", regex=r'(.*).py'
    )

    assert_rule_attributes(instance, attributes)

  def test_initialize__defined__attributes(
      self,
      concrete_rule_regex_base_instance: RuleRegexBase,
      concrete_rule_regex_base_class: Type[RuleRegexBase],
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "a concrete regex hint",
        "internal_use_only": False,
        "matches": [],
        "name": "concrete name",
        "operation": concrete_rule_regex_base_class.operation,
        "regex": r'[a-z]+',
        "save": "save_id",
        "splits": {
            1: None
        },
        "yaml_example": "mocked_yaml_example_rule_regex",
    }

    assert_rule_attributes(concrete_rule_regex_base_instance, attributes)

  def test_initialize__inheritance(
      self,
      concrete_rule_regex_base_instance: RuleRegexBase,
  ) -> None:
    assert_operation_inheritance(
        concrete_rule_regex_base_instance,
        bases=(RuleBase, RuleRegexBase),
    )
