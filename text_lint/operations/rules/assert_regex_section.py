"""AssertRegexSection class."""

import re
from typing import TYPE_CHECKING

from text_lint.exceptions.rules import RuleViolation
from text_lint.operations.rules.bases import rule_regex_base
from text_lint.utilities.translations import _
from text_lint.utilities.whitespace import new_line

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: example assert regex section rule
  operation: assert_regex_section
  regex: "^([a-z\\\\s]+)\\n$"
  save: assert_regex_section_example
  splits:
    - group: 1

{options}

""".format(options=rule_regex_base.YAML_OPTIONS)


class AssertRegexSection(rule_regex_base.RuleRegexBase):
  """Assert a sequence of lines matches a regular expression.

  The regex will be evaluated until a blank line is encountered.
  """

  hint = _("sections must be separated and contain lines that match this regex")
  operation = "assert_regex_section"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Apply the AssertRegexSection rule logic."""

    for data in controller.textfile:

      if data == new_line():
        break

      match = re.match(self.regex, data)
      if not match:
        raise RuleViolation(
            rule=self,
            expected=self.regex.pattern,
            textfile=controller.textfile,
        )

      self.matches.append(match)
