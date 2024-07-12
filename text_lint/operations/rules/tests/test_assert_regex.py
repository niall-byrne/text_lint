"""Test AssertRegex class."""

from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.rules import (
    assert_is_rule_violation,
    assert_rule_attributes,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.rules import RuleViolation
from text_lint.operations.rules.bases.rule_base import RuleBase
from text_lint.operations.rules.bases.rule_regex_base import RuleRegexBase
from ..assert_regex import YAML_EXAMPLE, AssertRegex


class TestAssertRegex:
  """Test the AssertRegex class."""

  def test_initialize__defaults__attributes(self) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "this line must match the regex",
        "internal_use_only": False,
        "matches": [],
        "name": "example assert regex rule",
        "operation": "assert_regex",
        "regex": "^([a-z-]+):\\s.+\n$",
        "save": None,
        "splits": {},
        "yaml_example": YAML_EXAMPLE,
    }

    instance = AssertRegex(
        name="example assert regex rule",
        regex="^([a-z-]+):\\s.+\n$",
    )

    assert_rule_attributes(instance, attributes)

  def test_initialize__defined__attributes(
      self,
      assert_regex_instance: AssertRegex,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "this line must match the regex",
        "internal_use_only": False,
        "matches": [],
        "name": "example assert regex rule",
        "operation": "assert_regex",
        "regex": "^([a-z-]+):\\s.+\n$",
        "save": "example",
        "splits": {
            1: " "
        },
        "yaml_example": YAML_EXAMPLE,
    }

    assert_rule_attributes(assert_regex_instance, attributes)

  def test_initialize__translations(
      self,
      assert_regex_instance: AssertRegex,
  ) -> None:
    assert_is_translated(assert_regex_instance.hint)

  def test_initialize__inheritance(
      self,
      assert_regex_instance: AssertRegex,
  ) -> None:
    assert_operation_inheritance(
        assert_regex_instance,
        bases=(
            RuleBase,
            RuleRegexBase,
            AssertRegex,
        ),
    )

  def test_apply__matches__stores_result(
      self,
      assert_regex_instance: AssertRegex,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.__next__.return_value = "matching: string\n"

    assert_regex_instance.apply(mocked_controller)

    assert len(assert_regex_instance.matches) == 1
    assert assert_regex_instance.matches[0].group(1) == "matching"

  def test_apply__does_not_match__raises_exception(
      self,
      assert_regex_instance: AssertRegex,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.index = 1
    mocked_textfile.__next__.return_value = "non matching string\n"

    with pytest.raises(RuleViolation) as exc:
      assert_regex_instance.apply(mocked_controller)

    assert len(assert_regex_instance.matches) == 0
    assert_is_rule_violation(
        exc=exc,
        rule=assert_regex_instance,
        textfile=mocked_textfile,
        expected=assert_regex_instance.regex.pattern,
    )
