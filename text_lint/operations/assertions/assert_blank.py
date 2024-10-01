"""AssertBlank class."""

from typing import TYPE_CHECKING

from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller.states.assertion import AssertionState

YAML_EXAMPLE = """

- name: example assert blank assertion
  operation: assert_blank

"""


class AssertBlank(AssertionBase):
  """Assert that the line is blank."""

  hint = _("the line contains no text")
  operation = "assert_blank"

  def __init__(
      self,
      name: str,
  ) -> None:
    super().__init__(name, None, None)

  def apply(
      self,
      state: "AssertionState",
  ) -> None:
    """Apply the AssertBlank assertion logic."""

    data = state.next()

    if data != "":
      state.fail("")
