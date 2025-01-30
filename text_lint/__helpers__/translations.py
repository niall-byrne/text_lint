"""Shared translation testing helpers."""

from typing import Any, List, Sequence

from text_lint.conftest import TRANSLATION_MARKER, mocked_t
from text_lint.operations.assertions.bases.assertion_regex_base import (
    YAML_ASSERTION_REGEX_EXAMPLE_OPTIONS,
)
from text_lint.operations.bases.operation_base import YAML_EXAMPLE_SECTIONS
from text_lint.utilities.translations import f as translation_f


class TranslationsCapture:
  """Extract interpolated translation strings."""

  def __init__(self) -> None:
    """Instantiate TranslationsCapture instances."""
    self._expected_translations: List[str] = []

  def assert_all_translated(self) -> None:
    assert_all_translated(self._expected_translations)

  # pylint: disable=invalid-name
  def f(self, *args: Any, nl: int = 0, **kwargs: Any) -> str:
    self._expected_translations.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)


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
