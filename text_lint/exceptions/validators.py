"""Exceptions for the text_lint result validators."""
from typing import TYPE_CHECKING

from text_lint.utilities.translations import _, f
from text_lint.utilities.whitespace import make_visible

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.validators.bases.validator_base import (
      ValidatorBase,
  )


class ValidationExceptionBase(ValueError):
  """Base class for validation exceptions."""


class ValidationFailure(ValidationExceptionBase):
  """Raised when a validation operation fails."""

  msg_fmt_validation_operation = _("  VALIDATION OPERATION: {0}")
  msg_fmt_validation_schema_operation_name = _("  SCHEMA OPERATION NAME: {0}")
  msg_fmt_validation_detail = _("  DETAIL: {0}")
  msg_fmt_validation_hint = _("  HINT: '{0}'")

  def __init__(
      self,
      description: str,
      detail: str,
      validator: "ValidatorBase",
  ) -> None:
    message = description
    message += f(
        self.msg_fmt_validation_operation,
        validator.__class__.__name__,
        nl=1,
    )
    message += f(
        self.msg_fmt_validation_schema_operation_name,
        make_visible(validator.name),
        nl=1,
    )
    message += f(
        self.msg_fmt_validation_detail,
        detail,
    )
    message += f(
        self.msg_fmt_validation_hint,
        validator.hint,
        nl=1,
    )

    super().__init__(message)
