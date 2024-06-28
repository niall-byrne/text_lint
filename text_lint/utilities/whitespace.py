"""Generic whitespace utilities."""

from typing import Any

from text_lint.config import NEW_LINE


def make_visible(value: Any) -> str:
  """Make a string's whitespace visible."""

  string = str(value). \
      replace("\n", "\\n"). \
      replace("\r", "\\r"). \
      replace("\t", "\\t")

  return string


def new_line(value: Any = None) -> str:
  if value:
    return str(value) + NEW_LINE
  return NEW_LINE
