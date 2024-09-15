"""AssertRegex class."""

import re
from typing import TYPE_CHECKING

from text_lint.operations.assertions.bases import assertion_regex_base
from text_lint.operations.bases.operation_base import YAML_EXAMPLE_SECTIONS
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import AssertionState

YAML_EXAMPLE_COMPONENTS = (
    _("example assert regex assertion"),
)
YAML_EXAMPLE = """

- name: {0}
  operation: assert_regex
  regex: "^([a-z-]+):\\\\s.+$"
  save: assert_regex_example
  splits:
    - group: 1
    - separator: "-"

{options_section}:
{options}

""".format(  # pylint: disable=duplicate-code
    *YAML_EXAMPLE_COMPONENTS,
    **YAML_EXAMPLE_SECTIONS,
    options=assertion_regex_base.YAML_ASSERTION_REGEX_EXAMPLE_OPTIONS,
)


class AssertRegex(assertion_regex_base.AssertionRegexBase):
  """Assert that the line matches a regular expression."""

  hint = _("this line must match the regex")
  operation = "assert_regex"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      state: "AssertionState",
  ) -> None:
    """Apply the AssertRegex assertion logic."""

    data = state.next()
    match = re.match(self.regex, data)

    if not match:
      state.fail(self.regex.pattern)
    else:
      state.save(match)
