"""Whitespace utilities."""

from typing import Any

from text_lint.config import NEW_LINE


def make_visible(value: Any) -> str:
  """Make the whitespace in an object's string representation visible.

  :param value: The object with a representation to make whitespace visible.
  :returns: A string representation of the object with whitespace visible.
  """
  string = str(value). \
      replace("\n", "\\n"). \
      replace("\r", "\\r"). \
      replace("\t", "\\t")

  return string


def new_line(value: Any = None) -> str:
  """Append a new line to an object's string representation.

  :param value: The object with a representation to append a new line to.
  :returns: A string representation of the object with an appended new line.
  """
  if value:
    return str(value) + NEW_LINE
  return NEW_LINE
