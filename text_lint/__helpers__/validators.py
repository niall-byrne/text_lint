"""Shared validator testing helpers."""

from typing import Any, Tuple

import pytest
from text_lint.__helpers__.translations import assert_all_translated
from text_lint.exceptions.validators import ValidationFailure
from text_lint.operations.validators.bases.validator_base import ValidatorBase
from text_lint.utilities.translations import f as translation_f
from text_lint.utilities.whitespace import make_visible


def assert_is_validation_failure(
    exc: pytest.ExceptionInfo[ValidationFailure],
    description_t: Tuple[Any, ...],
    detail_t: Tuple[Any, ...],
    validator: "ValidatorBase",
) -> None:
  expected_translations = []

  def f(*args: Any, nl: int = 0, **kwargs: Any) -> str:
    expected_translations.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)

  message = f(*description_t, nl=1)
  message += f(
      ValidationFailure.msg_fmt_validation_operation,
      validator.__class__.__name__,
      nl=1,
  )
  message += f(
      ValidationFailure.msg_fmt_validation_schema_operation_name,
      make_visible(validator.name),
      nl=1,
  )
  message += f(
      ValidationFailure.msg_fmt_validation_detail,
      translation_f(*detail_t),
      nl=1,
  )
  message += f(
      ValidationFailure.msg_fmt_validation_hint,
      validator.hint,
      nl=1,
  )

  assert exc.value.__class__ == ValidationFailure
  assert exc.value.args[0] == message
  assert_all_translated(expected_translations)
