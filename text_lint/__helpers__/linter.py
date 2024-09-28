"""Shared linter testing helpers."""
import os
from typing import TYPE_CHECKING, Any

import pytest
from text_lint.__helpers__.translations import assert_all_translated
from text_lint.exceptions.linter import LinterRecursionLimitExceeded
from text_lint.utilities.translations import f as translation_f
from text_lint.utilities.whitespace import make_visible

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter import Linter


def assert_is_linter_recursion_limit_exceeded(
    exc: pytest.ExceptionInfo[LinterRecursionLimitExceeded],
    linter: "Linter",
) -> None:
  expected_translation = []

  def f(*args: Any, nl: int = 0, **kwargs: Any) -> str:
    expected_translation.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)

  message = f(
      LinterRecursionLimitExceeded.msg_fmt_description,
      nl=1,
  )
  message += f(
      LinterRecursionLimitExceeded.msg_fmt_source_file,
      os.path.abspath(linter.textfile.path),
      nl=1,
  )
  message += f(
      LinterRecursionLimitExceeded.msg_fmt_assertion_name,
      linter.assertions.current.name,
      nl=1,
  )
  message += f(
      LinterRecursionLimitExceeded.msg_fmt_file_line,
      make_visible(linter.textfile.current),
      nl=1,
  )
  message += f(
      LinterRecursionLimitExceeded.msg_fmt_file_line_number,
      linter.textfile.index + 1,
      nl=1,
  )
  message += f(
      LinterRecursionLimitExceeded.msg_fmt_hint,
      nl=1,
  )

  assert exc.value.__class__ == LinterRecursionLimitExceeded
  assert exc.value.args[0] == message
  assert_all_translated(expected_translation)
