"""Exceptions for text file parser assertions."""

import os
from typing import TYPE_CHECKING

from text_lint.utilities.translations import _, f
from text_lint.utilities.whitespace import make_visible

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )
  from text_lint.sequencers.textfile import TextFileSequencer


class AssertionExceptionBase(ValueError):
  """Base class for parser assertion exceptions."""


class AssertionViolation(AssertionExceptionBase):
  """Raised when a parser assertion fails."""

  msg_fmt_assertion_operation = _("ASSERTION VIOLATION: {0}")
  msg_fmt_source_file = _("  SOURCE FILE: {0}")
  msg_fmt_assertion_name = _("  ASSERTION: '{0}'")
  msg_fmt_expected = _("  EXPECTED: '{0}'")
  msg_fmt_file_line = _("  FILE LINE: '{0}'")
  msg_fmt_file_line_number = _("  FILE LINE NUMBER: {0}")
  msg_fmt_hint = _("  HINT: '{0}'")

  def __init__(
      self,
      assertion: "AssertionBase",
      expected: str,
      textfile: "TextFileSequencer",
  ) -> None:
    message = f(self.msg_fmt_assertion_operation, assertion.operation, nl=1)
    message += f(
        self.msg_fmt_source_file,
        os.path.abspath(textfile.path),
        nl=1,
    )
    message += f(self.msg_fmt_assertion_name, assertion.name, nl=1)
    message += f(self.msg_fmt_expected, make_visible(expected), nl=1)
    message += f(self.msg_fmt_file_line, make_visible(textfile.current), nl=1)
    message += f(self.msg_fmt_file_line_number, textfile.index + 1, nl=1)
    message += f(self.msg_fmt_hint, assertion.hint, nl=1)
    super().__init__(message)


class AssertionCaptureGroupNotFound(AssertionExceptionBase):
  """Raised when an assertion references a non-existent capture group."""

  msg_fmt_assertion_operation = _("CAPTURE GROUP NOT FOUND: {0}")
  msg_fmt_assertion_name = _("  ASSERTION: '{0}'")
  msg_fmt_capture_group = _("  CAPTURE GROUP: '{0}'")
  msg_fmt_hint = _("  HINT: 'This capture group does not seem to exist.'")

  def __init__(
      self,
      assertion: "AssertionBase",
      capture_group: int,
  ) -> None:
    message = f(self.msg_fmt_assertion_operation, assertion.operation, nl=1)
    message += f(self.msg_fmt_assertion_name, assertion.name, nl=1)
    message += f(self.msg_fmt_capture_group, make_visible(capture_group), nl=1)
    message += f(self.msg_fmt_hint, [], nl=1)
    super().__init__(message)
