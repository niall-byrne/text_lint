"""ValidateDebug class."""

import json
from typing import TYPE_CHECKING

from text_lint.operations.validators.args.lookup_expression import (
    LookupExpressionSetArg,
)
from text_lint.operations.validators.bases.validator_base import ValidatorBase
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import ValidatorState
  from text_lint.operations.validators.args.lookup_expression import (
      AliasYamlLookupExpressionSet,
  )

YAML_EXAMPLE = """

- name: debug validator example
  operation: validate_debug
  saved:
    - source1.capture(1)
    - source2.capture(1)

"""


class ValidateDebug(ValidatorBase):
  """A validator to display result lookups."""

  hint = _("output save id lookups to the console")
  operation = "validate_debug"
  yaml_example = YAML_EXAMPLE

  msg_fmt_debug = _("DEBUG: '{0}'")

  def __init__(self, name: str, saved: "AliasYamlLookupExpressionSet"):
    super().__init__(name)
    self.lookup_expressions = LookupExpressionSetArg.create(saved)

  def apply(self, state: "ValidatorState") -> None:
    """Apply the ValidateDebug validator logic."""

    for requested_lookup_to_debug in self.lookup_expressions:

      result = state.lookup_expression(requested_lookup_to_debug)

      state.log(
          f(
              self.msg_fmt_debug,
              requested_lookup_to_debug.name,
          ),
          indent=True,
      )
      state.log(json.dumps(result, indent=4, default=str))
