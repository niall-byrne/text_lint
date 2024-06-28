"""Shared lookups testing helpers."""

from typing import Any, Tuple

import pytest
from text_lint.__helpers__.translations import assert_all_translated
from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.lookups import LookupFailure, LookupUnknown
from text_lint.operations.lookups.bases.lookup_base import LookupBase
from text_lint.utilities.translations import f as translation_f
from text_lint.utilities.whitespace import make_visible


def assert_is_lookup_failure(
    exc: pytest.ExceptionInfo[LookupFailure],
    description_t: Tuple[Any, ...],
    lookup: "LookupBase",
) -> None:
  expected_translation = []

  def f(*args: Any, nl: int = 0, **kwargs: Any) -> str:
    expected_translation.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)

  message = f(*description_t, nl=1)
  message += f(
      LookupFailure.msg_fmt_lookup_operation,
      lookup.__class__.__name__,
      nl=1,
  )
  message += f(
      LookupFailure.msg_fmt_schema_operation_name,
      lookup.requesting_operation_name,
      nl=1,
  )
  message += f(
      LookupFailure.msg_fmt_lookup_definition,
      nl=1,
  )
  message += f(
      LookupFailure.msg_fmt_result_source,
      make_visible(lookup.result_set.source),
      nl=1,
  )
  message += f(
      LookupFailure.msg_fmt_lookups,
      make_visible(lookup.result_set.lookups),
      nl=1,
  )
  message += f(
      LookupFailure.msg_fmt_failed_lookup,
      lookup.lookup_name,
      nl=1,
  )
  message += f(
      LookupFailure.msg_fmt_hint,
      lookup.hint,
      nl=1,
  )

  assert exc.value.__class__ == LookupFailure
  assert exc.value.args[0] == message
  assert_all_translated(expected_translation)


def assert_is_lookup_unknown(
    exc: pytest.ExceptionInfo[LookupUnknown],
    lookup: "LookupBase",
) -> None:
  expected_translation = []

  def f(*args: Any, nl: int = 0, **kwargs: Any) -> str:
    expected_translation.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)

  message = f(
      LookupUnknown.msg_fmt_lookup_unknown_description,
      nl=1,
  )
  message += f(
      LookupUnknown.msg_fmt_lookup_operation,
      lookup.__class__.__name__,
      nl=1,
  )
  message += f(
      LookupUnknown.msg_fmt_schema_operation_name,
      make_visible(lookup.requesting_operation_name),
      nl=1,
  )
  message += f(
      LookupUnknown.msg_fmt_lookup_definition,
      nl=1,
  )
  message += f(
      LookupUnknown.msg_fmt_result_source,
      make_visible(lookup.result_set.source),
      nl=1,
  )
  message += f(
      LookupUnknown.msg_fmt_lookups,
      make_visible(lookup.result_set.lookups),
      nl=1,
  )
  message += f(
      LookupUnknown.msg_fmt_failed_lookup,
      make_visible(lookup.lookup_name),
      nl=1,
  )
  message += f(
      LookupUnknown.msg_fmt_hint,
      LookupUnknown.msg_fmt_lookup_unknown_hint.
      format(LOOKUP_STATIC_VALUE_MARKER),
      nl=1,
  )

  assert exc.value.__class__ == LookupUnknown
  assert exc.value.args[0] == message
  assert_all_translated(expected_translation)
