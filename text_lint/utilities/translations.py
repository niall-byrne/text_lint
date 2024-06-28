"""Translation utilities."""

from gettext import gettext
from typing import Any

from text_lint.config import NEW_LINE


def f_string(string: str, *args: Any, nl: int = 0, **kwargs: Any) -> str:
  """Format style string interpolation.

  :param string: The string to interpolate.
  :param args: The positional arguments for format.
  :param nl: The number of newlines to add to the end of the string.
  :param kwargs: The keyword arguments for format.
  """

  return string.format(*args, **kwargs) + (NEW_LINE * nl)


f = f_string
_ = gettext
