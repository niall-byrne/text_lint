"""AssertBlank class."""

from typing import TYPE_CHECKING

from text_lint.exceptions.rules import RuleViolation
from text_lint.operations.rules.bases.rule_base import RuleBase
from text_lint.utilities.translations import _
from text_lint.utilities.whitespace import new_line

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: example assert blank rule
  operation: assert_blank

"""


class AssertBlank(RuleBase):
  """Assert that the line is blank."""

  hint = _("sections must be separated by blank lines")
  operation = "assert_blank"

  def __init__(
      self,
      name: str,
  ) -> None:
    super().__init__(name, None, None)

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Apply the AssertBlank rule logic."""

    data = next(controller.textfile)

    if new_line() != data:
      raise RuleViolation(
          rule=self,
          expected=new_line(),
          textfile=controller.textfile,
      )
