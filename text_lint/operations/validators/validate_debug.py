"""ValidateDebug class."""

import json
from typing import TYPE_CHECKING

from text_lint.operations.validators.args.result_set import ResultSetArg
from text_lint.operations.validators.bases.validator_base import ValidationBase
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller
  from text_lint.operations.validators.args.result_set import AliasYamlResultSet

YAML_EXAMPLE = """

- name: debug validator example
  operation: validate_debug
  saved:
    - source1.capture
    - source2.capture

"""


class ValidateDebug(ValidationBase):
  """A validator to display result lookups."""

  hint = _("outputs result values to the console")
  operation = "validate_debug"
  yaml_example = YAML_EXAMPLE

  msg_fmt_debug = _("DEBUG: '{0}'")

  def __init__(self, name: str, saved: "AliasYamlResultSet"):
    super().__init__(name)
    self.saved_results = ResultSetArg.create(saved)

  def apply(self, controller: "Controller") -> None:
    """Apply the ValidateDebug validator logic."""

    for requested_lookup_to_debug in self.saved_results:

      result = controller.forest.lookup(
          controller,
          requested_lookup_to_debug,
          self.name,
      )

      self.print(f(
          self.msg_fmt_debug,
          requested_lookup_to_debug.name,
      ))
      self.print(json.dumps(result, indent=4, default=str))
