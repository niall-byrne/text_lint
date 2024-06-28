"""AssertRegex class."""

import re
from typing import TYPE_CHECKING

from text_lint.exceptions.rules import RuleViolation
from text_lint.operations.rules.bases import rule_regex_base
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: example assert regex rule
  operation: assert_regex
  regex: "^([a-z-]+):\\s.+$\n"
  save: assert_regex_example
  splits:
    - group: 1
    - separator: "-"

{options}

""".format(options=rule_regex_base.YAML_OPTIONS)


class AssertRegex(rule_regex_base.RuleRegexBase):
  """Assert that the line matches a regular expression."""

  hint = _("this line must match the regex")
  operation = "assert_regex"

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Apply the AssertRegex rule logic."""

    data = next(controller.textfile)
    match = re.match(self.regex, data)

    if not match:
      # pylint: disable=duplicate-code
      raise RuleViolation(
          rule=self,
          expected=self.regex.pattern,
          textfile=controller.textfile,
      )

    self.matches = [match]
