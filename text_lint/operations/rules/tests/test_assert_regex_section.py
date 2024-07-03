"""Test AssertRegexSection class."""

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
from text_lint.utilities.whitespace import new_line
from ..assert_regex_section import YAML_EXAMPLE, AssertRegexSection


class TestAssertRegexSection:
  """Test the AssertRegexSection class."""

  def test_initialize__defaults__attributes(self) -> None:
    attributes: AliasOperationAttributes = {
        "hint":
            (
                "sections must be separated and contain lines that match "
                "this regex"
            ),
        "matches": [],
        "name": "example assert regex section rule",
        "operation": "assert_regex_section",
        "regex": "^([a-z-]+):\\s(.+)\n$",
        "save": None,
        "splits": {},
        "yaml_example": YAML_EXAMPLE,
    }

    instance = AssertRegexSection(
        name="example assert regex section rule",
        regex="^([a-z-]+):\\s(.+)\n$",
    )

    assert_rule_attributes(instance, attributes)

  def test_initialize__defined__attributes(
      self,
      assert_regex_section_instance: AssertRegexSection,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint":
            (
                "sections must be separated and contain lines that match "
                "this regex"
            ),
        "matches": [],
        "name": "example assert regex section rule",
        "operation": "assert_regex_section",
        "regex": "^([a-z-]+):\\s(.+)\n$",
        "save": "example",
        "splits": {
            2: None
        },
        "yaml_example": YAML_EXAMPLE,
    }

    assert_rule_attributes(assert_regex_section_instance, attributes)

  def test_initialize__translations(
      self,
      assert_regex_section_instance: AssertRegexSection,
  ) -> None:
    assert_is_translated(assert_regex_section_instance.hint)

  def test_initialize__inheritance(
      self,
      assert_regex_section_instance: AssertRegexSection,
  ) -> None:
    assert_operation_inheritance(
        assert_regex_section_instance,
        bases=(
            RuleBase,
            RuleRegexBase,
            AssertRegexSection,
        )
    )

  def test_apply__one_line__matches__stores_result(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.__iter__.return_value = [
        "matching: string\n",
        new_line(),
    ]

    assert_regex_section_instance.apply(mocked_controller)

    assert len(assert_regex_section_instance.matches) == 1
    assert assert_regex_section_instance.matches[0].group(1) == "matching"

  def test_apply__two_line__matches__stores_result(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.__iter__.return_value = [
        "matching-one: string\n",
        "matching-two: string\n",
        new_line(),
    ]

    assert_regex_section_instance.apply(mocked_controller)

    assert len(assert_regex_section_instance.matches) == 2
    assert assert_regex_section_instance.matches[0].group(1) == "matching-one"
    assert assert_regex_section_instance.matches[1].group(1) == "matching-two"

  def test_apply__entire_file__matches__stores_result(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.__iter__.return_value = [
        "matching-one: string\n",
        "matching-two: string\n",
        "matching-three: string\n",
    ]

    assert_regex_section_instance.apply(mocked_controller)

    assert len(assert_regex_section_instance.matches) == 3
    assert assert_regex_section_instance.matches[0].group(1) == "matching-one"
    assert assert_regex_section_instance.matches[1].group(1) == "matching-two"
    assert assert_regex_section_instance.matches[2].group(1) == "matching-three"

  def test_apply__two_lines__one_matches__one_does_not_match__raises_exception(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.index = 1
    mocked_textfile.__iter__.return_value = [
        "matching-one: string\n",
        "matching2: string\n",
        new_line(),
    ]

    with pytest.raises(RuleViolation) as exc:
      assert_regex_section_instance.apply(mocked_controller)

    assert len(assert_regex_section_instance.matches) == 1
    assert assert_regex_section_instance.matches[0].group(1) == "matching-one"
    assert_is_rule_violation(
        exc=exc,
        rule=assert_regex_section_instance,
        textfile=mocked_textfile,
        expected=assert_regex_section_instance.regex.pattern,
    )
