"""Shared exception testing helpers."""

import os
from typing import Any, Dict, Optional, Tuple

import pytest
from text_lint.__helpers__.translations import TranslationsCapture
from text_lint.exceptions.schema import SchemaError
from text_lint.utilities.whitespace import make_visible


def assert_is_schema_error(
    exc: pytest.ExceptionInfo[SchemaError],
    description_t: Tuple[Any, ...],
    schema_path: str,
    assertion_definition: Optional[Dict[str, Any]] = None,
) -> None:
  captured = TranslationsCapture()

  message = captured.f(*description_t, nl=1)
  message += captured.f(
      SchemaError.msg_fmt_schema_file,
      os.path.abspath(schema_path),
      nl=1,
  )
  if assertion_definition:
    message += captured.f(
        SchemaError.msg_fmt_operation_definition,
        nl=1,
    )
    for key, value in assertion_definition.items():
      message += "    {key}: {value}\n".format(
          key=key,
          value=make_visible(value),
      )

  assert exc.value.__class__ == SchemaError
  assert exc.value.args[0] == message
  captured.assert_all_translated()
