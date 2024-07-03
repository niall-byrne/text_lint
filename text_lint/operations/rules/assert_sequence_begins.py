"""AssertSequenceBegins class."""

from typing import TYPE_CHECKING, List

from text_lint.operations.rules.bases.rule_base import RuleBase
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: example assert sequence begins rule
  operation: assert_sequence_begins
  count: 3
  rules:
    - name: example assert blank rule
      operation: assert_blank
    - name: example assert regex rule
      operation: assert_regex
      regex: "^([a-z-]+):\\\\s(.+)$\\n"
      save: example
      splits:
        - group: 1
        - character: "-"
        - group: 2

note: set count to 0 to disable the nested sequence of steps.
      set count to -1 to repeat the nested steps until the eof is reached.

"""


class AssertSequenceBegins(RuleBase):
  """Inform the parser to start repeating a list of rules."""

  hint = _("identify a repeating sequence of parser rules")
  operation = "assert_sequence_begins"
  yaml_example = YAML_EXAMPLE

  def __init__(
      self,
      name: str,
      rules: List[RuleBase],
      count: int,
  ) -> None:
    self.count = count
    self.rules = rules
    super().__init__(name, None, None)

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Apply the AssertSequenceBegins rule logic."""

    if self.count == -1 or self.count > 0:
      controller.rules.start_repeating(self.count)
      controller.rules.insert(self.rules)
