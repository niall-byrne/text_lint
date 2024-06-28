"""AssertSequenceBegins class."""

from typing import TYPE_CHECKING, List

from text_lint.config import LOOP_COUNT
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import AssertionState

YAML_EXAMPLE = """

- name: example assert sequence begins assertion
  operation: assert_sequence_begins
  count: 3
  assertions:
    - name: example assert blank assertion
      operation: assert_blank
    - name: example assert regex assertion
      operation: assert_regex
      regex: "^([a-z-]+):\\s(.+)$"
      save: example
      splits:
        - group: 1
        - character: "-"
        - group: 2

note: Set count to 0 to disable the nested assertions.
      Set count to {LOOP_COUNT} to repeat the nested assertions until EOF.

""".format(LOOP_COUNT=LOOP_COUNT)


class AssertSequenceBegins(AssertionBase):
  """Inform the linter to start repeating a list of assertions."""

  hint = _("identify a repeating sequence of assertions")
  operation = "assert_sequence_begins"

  def __init__(
      self,
      name: str,
      assertions: List[AssertionBase],
      count: int,
  ) -> None:
    self.count = count
    self.assertions = assertions
    super().__init__(name, None, None)

  def apply(
      self,
      state: "AssertionState",
  ) -> None:
    """Apply the AssertSequenceBegins assertion logic."""

    state.loop(self.assertions, self.count)
