"""Shared translation testing helpers."""

from typing import List

from text_lint.conftest import TRANSLATION_MARKER, mocked_t


def as_translation(string: str) -> str:
  return TRANSLATION_MARKER + string


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


def assert_all_translated(strings: List[str]) -> None:
  for string in strings:
    assert_is_translated(string)
