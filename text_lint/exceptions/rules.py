"""Exceptions for text file parser rules."""

import os
from typing import TYPE_CHECKING

from text_lint.utilities.translations import _, f
from text_lint.utilities.whitespace import make_visible

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.rules.bases.rule_base import RuleBase
  from text_lint.sequencers.textfile import TextFileSequencer


class RuleExceptionBase(ValueError):
  """Base class for parser rule exceptions."""


class RuleViolation(RuleExceptionBase):
  """Raised when a text file parser rule fails."""

  msg_fmt_rule_operation = _("RULE VIOLATION: {0}")
  msg_fmt_source_file = _("  SOURCE FILE: {0}")
  msg_fmt_rule_name = _("  RULE: '{0}'")
  msg_fmt_expected = _("  EXPECTED: '{0}'")
  msg_fmt_file_line = _("  FILE LINE: '{0}'")
  msg_fmt_file_line_number = _("  FILE LINE NUMBER: {0}")
  msg_fmt_hint = _("  HINT: '{0}'")

  def __init__(
      self,
      rule: "RuleBase",
      expected: str,
      textfile: "TextFileSequencer",
  ) -> None:

    textfile.index -= 1

    message = f(self.msg_fmt_rule_operation, rule.operation, nl=1)
    message += f(
        self.msg_fmt_source_file,
        os.path.abspath(textfile.path),
        nl=1,
    )
    message += f(self.msg_fmt_rule_name, rule.name, nl=1)
    message += f(self.msg_fmt_expected, make_visible(expected), nl=1)
    message += f(self.msg_fmt_file_line, make_visible(textfile.current), nl=1)
    message += f(self.msg_fmt_file_line_number, textfile.index + 1, nl=1)
    message += f(self.msg_fmt_hint, rule.hint, nl=1)

    super().__init__(message)
