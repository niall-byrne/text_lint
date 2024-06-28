"""AssertSequenceEnds class."""

from typing import TYPE_CHECKING

from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: example assert sequence ends assertion
  operation: assert_sequence_ends

note: This assertion is used internally by text_lint to control iteration.
      It's not intended to be used directly in schemas.

"""


class AssertSequenceEnds(AssertionBase):
  """Inform the parser to stop repeating assertions."""

  hint = _("reserved")
  operation = "assert_sequence_ends"

  def __init__(
      self,
      name: str,
  ) -> None:
    super().__init__(name, None, None)

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Apply the AssertSequenceEnds assertion logic."""

    controller.assertions.stop_repeating()
