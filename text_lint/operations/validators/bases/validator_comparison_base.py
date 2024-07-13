"""ValidationComparisonBase class."""

import abc
from typing import TYPE_CHECKING

from text_lint.exceptions.validators import ValidationFailure
from text_lint.operations.validators.args.result_set import ResultSetArg
from text_lint.operations.validators.bases.validator_base import ValidationBase
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller
  from text_lint.operations.validators.args.result_set import (
      AliasYamlResultSet,
      ResultSet,
  )
  from text_lint.results.forest import AliasLookupResult


class ValidationComparisonBase(ValidationBase, abc.ABC):
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
      saved_a: "AliasYamlResultSet",
      saved_b: "AliasYamlResultSet",
  ):
    super().__init__(name)
    self.saved_results_a = ResultSetArg.create(saved_a)
    self.saved_results_b = ResultSetArg.create(saved_b)

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
      requested_result_a: "ResultSet",
      requested_result_b: "ResultSet",
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

  def apply(self, controller: "Controller") -> None:
    """Apply the Validator logic."""

    self._validate_result_set_counts()

    for requested_result_a, requested_result_b in zip(
        self.saved_results_a,
        self.saved_results_b,
    ):
      result_a = controller.forest.lookup(
          controller,
          requested_result_a,
          self.name,
      )
      result_b = controller.forest.lookup(
          controller,
          requested_result_b,
          self.name,
      )
      if not self.comparison(result_a, result_b):
        raise self.create_validation_failure_exception(
            result_a=result_a,
            result_b=result_b,
            requested_result_a=requested_result_a,
            requested_result_b=requested_result_b,
        )
      self.print(
          f(
              self.msg_fmt_comparison_success,
              requested_result_a.name,
              requested_result_b.name,
          )
      )

  def _validate_result_set_counts(self,) -> None:
    count_a = len(self.saved_results_a)
    count_b = len(self.saved_results_b)

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
