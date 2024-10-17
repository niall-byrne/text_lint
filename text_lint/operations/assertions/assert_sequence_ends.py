"""AssertSequenceEnds class."""

from typing import TYPE_CHECKING

from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.bases.operation_base import YAML_EXAMPLE_SECTIONS
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import AssertionState

YAML_EXAMPLE_COMPONENTS = (
    _("example assert sequence ends assertion"),
    _("This assertion is used internally by text_lint to control iteration."),
    _("It's not intended to be used directly in schemas.")
)
YAML_EXAMPLE = """

- name: {0}
  operation: assert_sequence_ends

{notes_section}:
  - {1}
  - {2}

""".format(*YAML_EXAMPLE_COMPONENTS, **YAML_EXAMPLE_SECTIONS)


class AssertSequenceEnds(AssertionBase):
  """Inform the linter to stop repeating assertions."""

  hint = _("reserved")
  internal_use_only = True
  operation = "assert_sequence_ends"
  yaml_example = YAML_EXAMPLE

  def __init__(
      self,
      name: str,
  ) -> None:
    super().__init__(name, None, None)

  class Parameters:
    name = {"type": str}

  def apply(
      self,
      state: "AssertionState",
  ) -> None:
    """Apply the AssertSequenceEnds assertion logic."""
