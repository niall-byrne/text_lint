"""Exceptions for the text_lint results."""
from typing import TYPE_CHECKING

from text_lint.utilities.translations import _, f
from text_lint.utilities.whitespace import make_visible

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.validators.args.result_set import ResultSet


class ResultExceptionBase(ValueError):
  """Base class for results exceptions."""


class ResultDoesNotExist(ResultExceptionBase):
  """Raised when a request is made for a non-existent result."""

  msg_fmt_does_not_exist = _("The result you've requested does not exist.")
  msg_fmt_result_source = _("  RESULT SOURCE: '{0}'")
  msg_fmt_schema_operation_name = _("  SCHEMA OPERATION NAME: {0}")
  msg_fmt_lookup_definition = _("  LOOKUP DEFINITION:")
  msg_fmt_lookup_result_source = _("    RESULT SOURCE: '{0}'")
  msg_fmt_lookups = _("    LOOKUPS: {0}")
  msg_fmt_hint = _("    HINT: '{0}'")
  msg_fmt_does_not_exist_hint = _(
      'results are created when applying the "rules" section of the schema'
  )

  def __init__(
      self,
      result_set: "ResultSet",
      requesting_operation_name: str,
  ) -> None:
    message = f(
        self.msg_fmt_does_not_exist,
        nl=1,
    )
    message += f(
        self.msg_fmt_result_source,
        make_visible(result_set.source),
        nl=1,
    )
    message += f(
        self.msg_fmt_schema_operation_name,
        make_visible(requesting_operation_name),
        nl=1,
    )
    message += f(
        self.msg_fmt_lookup_definition,
        nl=1,
    )
    message += f(
        self.msg_fmt_lookup_result_source,
        make_visible(result_set.source),
        nl=1,
    )
    message += f(
        self.msg_fmt_lookups,
        make_visible(result_set.lookups),
        nl=1,
    )
    message += f(
        self.msg_fmt_hint,
        self.msg_fmt_does_not_exist_hint,
        nl=1,
    )
    super().__init__(message)
