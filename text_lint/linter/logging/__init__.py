"""Logger class."""

import sys
from typing import TYPE_CHECKING, Optional, Union, overload

from text_lint.config import (
    LOGGING_COLUMN1_WIDTH,
    LOGGING_COLUMN2_WIDTH,
    LOGGING_INDENT,
)
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.validators.bases.validator_base import ValidatorBase
from text_lint.utilities.translations import _
from text_lint.utilities.whitespace import new_line

if TYPE_CHECKING:  # no cover
  from typing import Literal

  from text_lint.linter import Linter


class Logger:
  """Console logger."""

  msg_fmt_log_section = "=== {0} ==="
  msg_fmt_log_validator_prefix = _("VALIDATE")
  msf_fmt_log_unsupported_object = _("ERROR: Cannot log object '{0}'")

  def __init__(self, linter: "Linter"):
    self.linter = linter

  @overload
  def __call__(
      self,
      obj: str,
      index: None = None,
      indent: bool = False,
      section: bool = False,
  ) -> None:
    ...

  @overload
  def __call__(
      self,
      obj: AssertionBase,
      index: int,
      indent: "Literal[False]" = False,
      section: "Literal[False]" = False,
  ) -> None:
    ...

  @overload
  def __call__(
      self,
      obj: ValidatorBase,
      index: None = None,
      indent: "Literal[False]" = False,
      section: "Literal[False]" = False,
  ) -> None:
    ...

  def __call__(
      self,
      obj: Union[str, AssertionBase, ValidatorBase],
      index: Optional[int] = None,
      indent: bool = False,
      section: bool = False,
  ) -> None:
    if isinstance(obj, str):
      self._log_string(obj, indent, section)
    elif isinstance(obj, AssertionBase) and index is not None:
      self._log_assertion(obj, index)
    elif isinstance(obj, ValidatorBase):
      self._log_validator(obj)
    else:
      self._log_string(
          self.msf_fmt_log_unsupported_object.format(str(obj)),
          indent=False,
          section=False,
      )

  def _log_string(
      self,
      message: str,
      indent: bool,
      section: bool,
  ) -> None:
    sys.stdout.write(
        new_line(self._indent(
            self._section(message, section),
            indent,
        ))
    )

  def _indent(self, message: str, indent: bool) -> str:
    if indent:
      return LOGGING_INDENT + message
    return message

  def _section(self, message: str, section: bool) -> str:
    if section:
      return self.msg_fmt_log_section.format(message)
    return message

  def _log_assertion(
      self,
      assertion: "AssertionBase",
      index: int,
  ) -> None:
    if index >= self.linter.textfile.index - 1:
      line_identifier = "{0}".format(index + 1)
    else:
      line_identifier = "{0}-{1}".format(
          index + 1,
          self.linter.textfile.index + 1,
      )

    self._log_string(
        line_identifier.ljust(LOGGING_COLUMN1_WIDTH) +
        self._operation_as_columns(assertion),
        indent=False,
        section=False,
    )

  def _log_validator(
      self,
      validator: "ValidatorBase",
  ) -> None:
    self._log_string(
        self.msg_fmt_log_validator_prefix.ljust(LOGGING_COLUMN1_WIDTH) +
        self._operation_as_columns(validator),
        indent=False,
        section=False,
    )

  def _operation_as_columns(
      self,
      operation: Union[AssertionBase, ValidatorBase],
  ) -> str:
    return operation.operation.ljust(LOGGING_COLUMN2_WIDTH) + operation.name
