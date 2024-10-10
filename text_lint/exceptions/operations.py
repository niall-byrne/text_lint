"""Exceptions for the text_lint generic operation classes."""

from typing import TYPE_CHECKING

from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class OperationExceptionBase(ValueError):
  """Base class for operation exceptions."""


class InvalidParameterValidation(OperationExceptionBase):
  """Raised when an operation's parameter validation is misconfigured."""

  msg_fmt_detail = _("  DETAIL: {0}")
  msg_fmt_operation_class = _("  OPERATION CLASS: {0}")

  def __init__(
      self,
      translated_description: str,
      translated_detail: str,
      operation_class: "Any",
  ) -> None:
    message = f(
        translated_description,
        nl=1,
    )
    message += f(
        self.msg_fmt_operation_class,
        operation_class.__name__,
        nl=1,
    )
    message += f(
        self.msg_fmt_detail,
        translated_detail,
        nl=1,
    )
    super().__init__(message)
