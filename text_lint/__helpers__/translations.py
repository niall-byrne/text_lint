"""Shared translation testing helpers."""

from typing import Sequence

from text_lint.conftest import TRANSLATION_MARKER, mocked_t
from text_lint.operations.assertions.bases.assertion_regex_base import (
    YAML_ASSERTION_REGEX_EXAMPLE_OPTIONS,
)
from text_lint.operations.bases.operation_base import YAML_EXAMPLE_SECTIONS


def as_translation(string: str) -> str:
  return TRANSLATION_MARKER + string


def assert_all_translated(strings: Sequence[str]) -> None:
  for string in strings:
    assert_is_translated(string)


def assert_all_translated_substrings(
    substrings: Sequence[str],
    string: str,
) -> None:
  for substring in substrings:
    assert_is_translated_substring(substring, string)


def assert_is_translated(string: str) -> None:
  if string.startswith(TRANSLATION_MARKER):
    try:
      mocked_t.assert_any_call(string[len(TRANSLATION_MARKER):])
      return
    except AssertionError:  # pragma: no cover
      pass
  raise AssertionError(  # pragma: no cover
    "UNTRANSLATED STRING: '{0}'".format(string)
  )


def assert_is_translated_substring(substring: str, string: str) -> None:
  assert_is_translated(substring)
  assert substring in string


def assert_is_translated_yaml_example(
    example: str,
    components: Sequence[str],
    notes: bool = False,
    assertion_options: bool = False,
) -> None:
  assert_all_translated_substrings(components, example)

  if notes:
    assert_is_translated_substring(
        YAML_EXAMPLE_SECTIONS["notes_section"],
        example,
    )
  else:
    assert YAML_EXAMPLE_SECTIONS["notes_section"] not in example

  if assertion_options:
    assert_is_translated_substring(
        YAML_EXAMPLE_SECTIONS["options_section"],
        example,
    )
    assert_is_translated_substring(
        YAML_ASSERTION_REGEX_EXAMPLE_OPTIONS,
        example,
    )
  else:
    assert YAML_EXAMPLE_SECTIONS["options_section"] not in example
