"""Shared assertions testing helpers."""
import os
import re
from typing import TYPE_CHECKING, Any, Dict, List
from unittest import mock

import pytest
from text_lint.__helpers__.translations import (
    as_translation,
    assert_all_translated,
)
from text_lint.exceptions.assertions import (
    AssertionCaptureGroupNotFound,
    AssertionLogicError,
    AssertionViolation,
)
from text_lint.operations.assertions.args.split import SplitArgs
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.assertions.bases.assertion_regex_base import (
    AssertionRegexBase,
)
from text_lint.utilities.translations import f as translation_f
from text_lint.utilities.whitespace import make_visible

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.sequencers.textfile import TextFileSequencer

AliasAssertionAttributes = Dict[str, Any]


def assert_assertion_attributes(
    assertion_instance: "AssertionBase",
    attributes: AliasAssertionAttributes,
) -> None:

  for attribute_name, attribute_value in attributes.items():
    attribute = getattr(assertion_instance, attribute_name)
    if attribute_name == "hint":
      assert attribute == as_translation(attribute_value)
    elif attribute_name == "splits":
      assert isinstance(attribute, SplitArgs)
      assert attribute.as_dict() == attribute_value
    elif attribute_name == "regex":
      assert isinstance(attribute, re.Pattern)
      assert attribute.pattern == attribute_value
    else:
      assert attribute == attribute_value


def assert_is_assertion_capture_group_not_found(
    exc: pytest.ExceptionInfo[AssertionCaptureGroupNotFound],
    assertion: "AssertionBase",
    capture_group: int,
) -> None:
  expected_translation = []

  def f(*args: Any, nl: int = 0, **kwargs: Any) -> str:
    expected_translation.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)

  message = f(
      AssertionCaptureGroupNotFound.msg_fmt_assertion_operation,
      assertion.operation,
      nl=1,
  )
  message += f(
      AssertionCaptureGroupNotFound.msg_fmt_assertion_name,
      assertion.name,
      nl=1,
  )
  message += f(
      AssertionCaptureGroupNotFound.msg_fmt_capture_group,
      make_visible(capture_group),
      nl=1,
  )
  message += f(
      AssertionCaptureGroupNotFound.msg_fmt_hint,
      assertion.hint,
      nl=1,
  )

  assert exc.value.__class__ == AssertionCaptureGroupNotFound
  assert exc.value.args[0] == message
  assert_all_translated(expected_translation)


def assert_is_assertion_logic_error(
    exc: pytest.ExceptionInfo[AssertionLogicError],
    assertion: "AssertionBase",
    textfile: "TextFileSequencer",
    hint: str,
) -> None:
  expected_translation = []

  def f(*args: Any, nl: int = 0, **kwargs: Any) -> str:
    expected_translation.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)

  message = f(
      AssertionLogicError.msg_fmt_assertion_operation,
      assertion.operation,
      nl=1,
  )
  message += f(
      AssertionLogicError.msg_fmt_source_file,
      os.path.abspath(textfile.path),
      nl=1,
  )
  message += f(
      AssertionLogicError.msg_fmt_assertion_name,
      assertion.name,
      nl=1,
  )
  message += f(
      AssertionLogicError.msg_fmt_file_line,
      make_visible(textfile.current),
      nl=1,
  )
  message += f(
      AssertionLogicError.msg_fmt_file_line_number,
      textfile.index + 1,
      nl=1,
  )
  message += f(
      AssertionLogicError.msg_fmt_hint,
      hint,
      nl=1,
  )

  assert exc.value.__class__ == AssertionLogicError
  assert exc.value.args[0] == message
  assert_all_translated(expected_translation)


def assert_is_assertion_violation(
    exc: pytest.ExceptionInfo[AssertionViolation],
    assertion: "AssertionBase",
    textfile: "TextFileSequencer",
    expected: str,
) -> None:
  expected_translation = []

  def f(*args: Any, nl: int = 0, **kwargs: Any) -> str:
    expected_translation.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)

  message = f(
      AssertionViolation.msg_fmt_assertion_operation,
      assertion.operation,
      nl=1,
  )
  message += f(
      AssertionViolation.msg_fmt_source_file,
      os.path.abspath(textfile.path),
      nl=1,
  )
  message += f(
      AssertionViolation.msg_fmt_assertion_name,
      assertion.name,
      nl=1,
  )
  message += f(
      AssertionViolation.msg_fmt_expected,
      make_visible(expected),
      nl=1,
  )
  message += f(
      AssertionViolation.msg_fmt_file_line,
      make_visible(textfile.current),
      nl=1,
  )
  message += f(
      AssertionViolation.msg_fmt_file_line_number,
      textfile.index + 1,
      nl=1,
  )
  message += f(
      AssertionViolation.msg_fmt_hint,
      assertion.hint,
      nl=1,
  )

  assert exc.value.__class__ == AssertionViolation
  assert exc.value.args[0] == message
  assert_all_translated(expected_translation)


def assert_state_saved(
    operation: "AssertionRegexBase",
    mocked_state: mock.Mock,
    matches: List[str],
) -> None:
  assert len(mocked_state.save.mock_calls) == 1
  assert len(mocked_state.save.mock_calls[0].args) == 1

  if isinstance(mocked_state.save.mock_calls[0].args[0], list):
    received_args = mocked_state.save.mock_calls[0].args[0]
    assert len(mocked_state.save.mock_calls[0].args[0]) == len(matches)
  else:
    received_args = [mocked_state.save.mock_calls[0].args[0]]

  for received, expected in zip(
      received_args,
      matches,
  ):
    assert received.string == expected
    assert received.re.pattern == operation.regex.pattern
