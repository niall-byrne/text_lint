"""Rule sequence integration testing."""

from typing import TYPE_CHECKING, Callable, List
from unittest import mock

from text_lint.config import NEW_LINE
from text_lint.operations.rules import (
    AssertBlank,
    AssertEqual,
    AssertSequenceBegins,
    AssertSequenceEnds,
)

if TYPE_CHECKING:
  from text_lint.operations.rules.bases.rule_base import RuleBase


class TestRuleSequences:
  """Rule sequence integration testing."""

  data_valid = (NEW_LINE + "a" + NEW_LINE) * 10

  def test_simple_sequence__correct_rule_sequence(
      self,
      create_mocked_controller: Callable[[str, str], mock.Mock],
      yaml_simple_sequence: str,
  ) -> None:
    expected_rules = [AssertSequenceBegins.operation]
    expected_rules += [
        AssertBlank.operation, AssertEqual.operation,
        AssertSequenceEnds.operation
    ] * 10
    expected_rules += [AssertSequenceEnds.operation]
    processed_rules: List["RuleBase"] = []
    controller = create_mocked_controller(yaml_simple_sequence, self.data_valid)

    for rule in controller.rules:
      rule.apply(controller)
      processed_rules.append(rule)

    assert len(processed_rules) == len(expected_rules)
    for processed_rule, expected_rule in zip(processed_rules, expected_rules):
      assert processed_rule.operation == expected_rule

  def test_nested_sequence__correct_rule_sequence(
      self,
      create_mocked_controller: Callable[[str, str], mock.Mock],
      yaml_nested_sequence: str,
  ) -> None:
    expected_rules = [AssertSequenceBegins.operation]
    expected_rules += [
        AssertSequenceBegins.operation, AssertBlank.operation,
        AssertEqual.operation, AssertSequenceEnds.operation,
        AssertSequenceEnds.operation
    ] * 10
    expected_rules += [AssertSequenceEnds.operation]
    processed_rules: List["RuleBase"] = []
    controller = create_mocked_controller(yaml_nested_sequence, self.data_valid)

    for rule in controller.rules:
      rule.apply(controller)
      processed_rules.append(rule)

    assert len(processed_rules) == len(expected_rules)
    for processed_rule, expected_rule in zip(processed_rules, expected_rules):
      assert processed_rule.operation == expected_rule

  def test_infinite_sequence__correct_rule_sequence(
      self,
      create_mocked_controller: Callable[[str, str], mock.Mock],
      yaml_infinite_sequence: str,
  ) -> None:
    expected_rules = [AssertSequenceBegins.operation]
    expected_rules += [
        AssertBlank.operation, AssertEqual.operation,
        AssertSequenceEnds.operation
    ] * 10
    processed_rules: List["RuleBase"] = []
    controller = create_mocked_controller(
        yaml_infinite_sequence, self.data_valid
    )

    while True:
      try:
        rule = next(controller.rules)
        rule.apply(controller)
        processed_rules.append(rule)
      except StopIteration:
        break

    assert len(processed_rules) == len(expected_rules)
    for processed_rule, expected_rule in zip(processed_rules, expected_rules):
      assert processed_rule.operation == expected_rule
