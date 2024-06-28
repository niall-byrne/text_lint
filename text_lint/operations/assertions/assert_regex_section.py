"""AssertRegexSection class."""

import re
from typing import TYPE_CHECKING, List, Match

from text_lint.exceptions.assertions import AssertionViolation
from text_lint.operations.assertions.bases import assertion_regex_base
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: example assert regex section assertion
  operation: assert_regex_section
  regex: "^([a-z\\s]+)$"
  save: assert_regex_section_example
  splits:
    - group: 1

{options}

""".format(options=assertion_regex_base.YAML_OPTIONS)


class AssertRegexSection(assertion_regex_base.AssertionRegexBase):
  """Assert a section of adjacent lines matches a regular expression.

  The regex will be evaluated until it no longer matches.
  """

  hint = _("one or more adjacent lines (the 'section') must match this regex")
  operation = "assert_regex_section"

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Apply the AssertRegexSection assertion logic."""

    section_detected = False
    matches: List[Match[str]] = []

    for data in controller.textfile:

      match = re.match(self.regex, data)

      if not match and not section_detected:
        raise AssertionViolation(
            assertion=self,
            expected=self.regex.pattern,
            textfile=controller.textfile,
        )

      if not match:
        # Another operation must check this line now.
        controller.textfile.index -= 1
        break

      matches.append(match)
      section_detected = True

    result_tree = self.create_result_tree(matches)
    controller.forest.add(result_tree)
