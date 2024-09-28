"""Exceptions for the linter."""

import os
from typing import TYPE_CHECKING

from text_lint.utilities.translations import _, f
from text_lint.utilities.whitespace import make_visible

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter import Linter


class LinterExceptionBase(ValueError):
  """Base class for linter exceptions."""


class LinterRecursionLimitExceeded(LinterExceptionBase):
  """Raised when a text line is read repeatedly past the recursion limit."""

  msg_fmt_description = _("RECURSION LIMIT REACHED")
  msg_fmt_source_file = _("  SOURCE FILE: {0}")
  msg_fmt_assertion_name = _("  ASSERTION: '{0}'")
  msg_fmt_file_line = _("  FILE LINE: '{0}'")
  msg_fmt_file_line_number = _("  FILE LINE NUMBER: {0}")
  msg_fmt_hint = _(
      "  HINT: 'There appears to be a non-matching unbounded loop "
      "in the assertions.'"
  )

  def __init__(self, linter: "Linter") -> None:
    message = f(self.msg_fmt_description, nl=1)
    message += f(
        self.msg_fmt_source_file,
        os.path.abspath(linter.textfile.path),
        nl=1,
    )
    message += f(
        self.msg_fmt_assertion_name,
        linter.assertions.current.name,
        nl=1,
    )
    message += f(
        self.msg_fmt_file_line,
        make_visible(linter.textfile.current),
        nl=1,
    )
    message += f(
        self.msg_fmt_file_line_number,
        linter.textfile.index + 1,
        nl=1,
    )
    message += f(self.msg_fmt_hint, nl=1)

    super().__init__(message)
