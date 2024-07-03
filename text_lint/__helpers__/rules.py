"""Shared rule testing helpers."""
import os
import re
from typing import TYPE_CHECKING, Any, Dict

import pytest
from text_lint.__helpers__.translations import (
    as_translation,
    assert_all_translated,
)
from text_lint.exceptions.rules import RuleViolation
from text_lint.operations.rules.args.split import SplitArgs
from text_lint.operations.rules.bases.rule_base import RuleBase
from text_lint.utilities.translations import f as translation_f
from text_lint.utilities.whitespace import make_visible
from .operations import REQUIRED_ATTRIBUTES

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.sequencers.textfile import TextFileSequencer

AliasRuleAttributes = Dict[str, Any]


def assert_is_rule_violation(
    exc: pytest.ExceptionInfo[RuleViolation],
    rule: "RuleBase",
    textfile: "TextFileSequencer",
    expected: str,
) -> None:
  expected_translation = []

  def f(*args: Any, nl: int = 0, **kwargs: Any) -> str:
    expected_translation.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)

  message = f(
      RuleViolation.msg_fmt_rule_operation,
      rule.operation,
      nl=1,
  )
  message += f(
      RuleViolation.msg_fmt_source_file,
      os.path.abspath(textfile.path),
      nl=1,
  )
  message += f(
      RuleViolation.msg_fmt_rule_name,
      rule.name,
      nl=1,
  )
  message += f(
      RuleViolation.msg_fmt_expected,
      make_visible(expected),
      nl=1,
  )
  message += f(
      RuleViolation.msg_fmt_file_line,
      make_visible(textfile.current),
      nl=1,
  )
  message += f(
      RuleViolation.msg_fmt_file_line_number,
      textfile.index + 1,
      nl=1,
  )
  message += f(
      RuleViolation.msg_fmt_hint,
      rule.hint,
      nl=1,
  )

  assert exc.value.__class__ == RuleViolation
  assert exc.value.args[0] == message
  assert_all_translated(expected_translation)


def assert_rule_attributes(
    rule_instance: "RuleBase",
    attributes: AliasRuleAttributes,
) -> None:

  for required_attribute in REQUIRED_ATTRIBUTES:
    assert required_attribute in attributes

  for attribute_name, attribute_value in attributes.items():
    attribute = getattr(rule_instance, attribute_name)
    if attribute_name == "hint":
      assert attribute == as_translation(attribute_value)
    elif attribute_name == "splits":
      assert isinstance(attribute, SplitArgs)
      assert attribute.as_dict() == attribute_value
    elif attribute_name == "regex":
      assert isinstance(attribute, re.Pattern)
      assert attribute.pattern == attribute_value
    else:
      assert attribute == attribute_value
