"""AssertEqual class."""

import re
from typing import TYPE_CHECKING, Optional

from text_lint.exceptions.rules import RuleViolation
from text_lint.operations.rules.bases import rule_regex_base
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller
  from text_lint.operations.rules.args.split import AliasYamlSplit

YAML_EXAMPLE = """

- name: example assert equal rule
  operation: assert_equal
  expected: "simple-string-MATCHING\n"
  case_insensitive: False
  save: assert_equal_example
  splits:
    - group: 1
    - separator: "-"

{options}
optional: 'case_insensitive' will match strings with differing cases.
          (This defaults to false.)

""".format(options=rule_regex_base.YAML_OPTIONS)


class AssertEqual(rule_regex_base.RuleRegexBase):
  """Assert that the line matches an expected static value."""

  hint = _("this line must match the expected value")
  operation = "assert_equal"

  def __init__(
      self,
      name: str,
      expected: str,
      save: Optional[str] = None,
      splits: Optional["AliasYamlSplit"] = None,
      case_sensitive: Optional[bool] = True,
  ) -> None:
    self.expected = expected
    self.case_sensitive = case_sensitive
    super().__init__(name, "(.*)", save, splits)

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Apply the AssertEqual rule logic."""

    data = next(controller.textfile)
    match = re.match(self.regex, data)

    equality_check: bool = False

    if match and not self.case_sensitive:
      equality_check = match.group(1).lower() == self.expected.lower()

    if match and self.case_sensitive:
      equality_check = match.group(1) == self.expected

    if not match or not equality_check:
      # pylint: disable=duplicate-code
      raise RuleViolation(
          rule=self,
          expected=self.expected,
          textfile=controller.textfile,
      )

    self.matches = [match]
