"""ValidateEqual class."""

from typing import TYPE_CHECKING

from text_lint.exceptions.validators import ValidationFailure
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

- name: equality validator example
  operation: validate_equal
  saved_a:
    - source1.capture
  saved_b:
    - source2.capture

"""


class ValidateEqual(ValidatorBase):
  """A validator to check equality between result lookups."""

  hint = _("validates equality between sets of values")
  operation = "validate_equal"

  msg_fmt_comparison_failure = _("'{0}' != '{1}'")
  msg_fmt_comparison_success = _("EQUAL: '{0}' == '{1}'")
  msg_fmt_set_count_failure_description = _("'{0}' != '{1}'")
  msg_fmt_set_count_failure_detail = _(
      "Mismatched result set counts are being compared."
  )

  def __init__(
      self,
      name: str,
      saved_a: "AliasYamlLookupExpressionSet",
      saved_b: "AliasYamlLookupExpressionSet",
  ):
    super().__init__(name)
    self.lookup_expression_set_a = LookupExpressionSetArg.create(saved_a)
    self.lookup_expression_set_b = LookupExpressionSetArg.create(saved_b)

  def apply(self, state: "ValidatorState") -> None:
    """Apply the ValidateEqual validator logic."""

    self._validate_result_set_counts()

    for lookup_expression_a, lookup_expression_b in zip(
        self.lookup_expression_set_a,
        self.lookup_expression_set_b,
    ):
      result_a = state.lookup_expression(lookup_expression_a)
      result_b = state.lookup_expression(lookup_expression_b)
      if result_a != result_b:
        raise ValidationFailure(
            description=f(
                self.msg_fmt_comparison_failure,
                lookup_expression_a.name,
                lookup_expression_b.name,
                nl=1,
            ),
            detail=f(
                self.msg_fmt_comparison_failure,
                result_a,
                result_b,
                nl=1,
            ),
            validator=self
        )
      state.log(
          f(
              self.msg_fmt_comparison_success,
              lookup_expression_a.name,
              lookup_expression_b.name,
          ),
          indent=True,
      )

  def _validate_result_set_counts(self,) -> None:
    count_a = len(self.lookup_expression_set_a)
    count_b = len(self.lookup_expression_set_b)

    if count_a != count_b:
      raise ValidationFailure(
          description=f(
              self.msg_fmt_set_count_failure_description,
              count_a,
              count_b,
              nl=1,
          ),
          detail=f(
              self.msg_fmt_set_count_failure_detail,
              nl=1,
          ),
          validator=self
      )
