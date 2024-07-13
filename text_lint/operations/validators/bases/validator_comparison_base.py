"""ValidationComparisonBase class."""

import abc
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
      LookupExpression,
  )
  from text_lint.results.forest import AliasLookupResult


class ValidationComparisonBase(ValidatorBase, abc.ABC):
  """A base validator to compare sets of result lookups."""

  msg_fmt_comparison_failure: str
  msg_fmt_comparison_success: str
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

  @abc.abstractmethod
  def comparison(
      self,
      result_a: "AliasLookupResult",
      result_b: "AliasLookupResult",
  ) -> bool:
    """Perform the result comparison between each result element."""

  def create_validation_failure_exception(
      self,
      result_a: "AliasLookupResult",
      result_b: "AliasLookupResult",
      requested_result_a: "LookupExpression",
      requested_result_b: "LookupExpression",
  ) -> ValidationFailure:
    """Create the appropriate validation failure exception."""

    return ValidationFailure(
        description=f(
            self.msg_fmt_comparison_failure,
            requested_result_a.name,
            requested_result_b.name,
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

  def apply(self, state: "ValidatorState") -> None:
    """Apply the Validator logic."""

    self._validate_result_set_counts()

    for lookup_expression_a, lookup_expression_b in zip(
        self.lookup_expression_set_a,
        self.lookup_expression_set_b,
    ):
      result_a = state.lookup_expression(lookup_expression_a)
      result_b = state.lookup_expression(lookup_expression_b)
      if not self.comparison(result_a, result_b):
        raise self.create_validation_failure_exception(
            result_a=result_a,
            result_b=result_b,
            requested_result_a=lookup_expression_a,
            requested_result_b=lookup_expression_b,
        )
      state.log(
          f(
              self.msg_fmt_comparison_success,
              lookup_expression_a.name,
              lookup_expression_b.name,
          ),
          indent=True,
      )

  def _validate_result_set_counts(self) -> None:
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
