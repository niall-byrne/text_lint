"""Shared validator testing helpers."""

from typing import Any, Protocol, Tuple, Type

import pytest
from text_lint.__helpers__.translations import TranslationsCapture
from text_lint.exceptions.validators import (
    ValidationExceptionBase,
    ValidationFailure,
    ValidationInvalidComparison,
)
from text_lint.operations.validators.bases.validator_base import ValidatorBase
from text_lint.utilities.translations import f as translation_f
from text_lint.utilities.whitespace import make_visible


class ValidationHelperFunctionType(Protocol):

  def __call__(
      self,
      exc: pytest.ExceptionInfo[ValidationExceptionBase],
      description_t: Tuple[Any, ...],
      detail_t: Tuple[Any, ...],
      validator: "ValidatorBase",
  ) -> None:
    ...


def validator_helper_factory(
    validation_error: Type[ValidationExceptionBase]
) -> ValidationHelperFunctionType:

  def validator_helper_function(
      exc: pytest.ExceptionInfo[ValidationExceptionBase],
      description_t: Tuple[Any, ...],
      detail_t: Tuple[Any, ...],
      validator: "ValidatorBase",
  ) -> None:
    captured = TranslationsCapture()

    message = captured.f(*description_t, nl=1)
    message += captured.f(
        ValidationFailure.msg_fmt_validation_operation,
        validator.__class__.__name__,
        nl=1,
    )
    message += captured.f(
        ValidationFailure.msg_fmt_validation_schema_operation_name,
        make_visible(validator.name),
        nl=1,
    )
    message += captured.f(
        ValidationFailure.msg_fmt_validation_detail,
        translation_f(*detail_t),
        nl=1,
    )
    message += captured.f(
        ValidationFailure.msg_fmt_validation_hint,
        validator.hint,
        nl=1,
    )

    assert exc.value.__class__ == validation_error
    assert exc.value.args[0] == message
    captured.assert_all_translated()

  return validator_helper_function


assert_is_validation_failure = validator_helper_factory(ValidationFailure)
assert_is_invalid_comparison = validator_helper_factory(
    ValidationInvalidComparison
)

validate_expression_with_numeric_lookup_results = pytest.mark.parametrize(
    "lookup_results",
    [(1, 2, 3, 4)],
    ids=str,
)
