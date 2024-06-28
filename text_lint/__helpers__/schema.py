"""Shared exception testing helpers."""

import os
from typing import Any, Dict, Optional, Tuple

import pytest
from text_lint.__helpers__.translations import assert_all_translated
from text_lint.exceptions.schema import SchemaError
from text_lint.utilities.translations import f as translation_f
from text_lint.utilities.whitespace import make_visible


def assert_is_schema_error(
    exc: pytest.ExceptionInfo[SchemaError],
    description_t: Tuple[Any, ...],
    schema_path: str,
    rule_definition: Optional[Dict[str, Any]] = None,
) -> None:
  expected_translation = []

  def f(*args: Any, nl: int = 0, **kwargs: Any) -> str:
    expected_translation.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)

  message = f(*description_t, nl=1)
  message += f(
      SchemaError.msg_fmt_schema_file,
      os.path.abspath(schema_path),
      nl=1,
  )
  if rule_definition:
    message += f(
        SchemaError.msg_fmt_operation_definition,
        nl=1,
    )
    for key, value in rule_definition.items():
      message += "    {key}: {value}\n".format(
          key=key,
          value=make_visible(value),
      )

  assert exc.value.__class__ == SchemaError
  assert exc.value.args[0] == message
  assert_all_translated(expected_translation)
