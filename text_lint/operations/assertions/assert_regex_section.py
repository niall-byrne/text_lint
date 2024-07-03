"""AssertRegexSection class."""

import re
from typing import TYPE_CHECKING, List, Match

from text_lint.operations.assertions.bases import assertion_regex_base
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import AssertionState

YAML_EXAMPLE = """

- name: example assert regex section assertion
  operation: assert_regex_section
  regex: "^([a-z\\\\s]+)$"
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
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      state: "AssertionState",
  ) -> None:
    """Apply the AssertRegexSection assertion logic."""

    matches: List[Match[str]] = []

    while True:

      try:
        data = state.next()
      except StopIteration:
        break

      match = re.match(self.regex, data)

      if match:
        matches.append(match)

      if not match:
        if not matches:
          state.fail(self.regex.pattern)
        else:
          # Another operation must check this line now.
          state.rewind()
          break

    state.save(matches)
