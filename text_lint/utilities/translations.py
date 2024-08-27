"""Translation utilities."""

import gettext
import locale
import os
from typing import Any

import text_lint
from text_lint.config import NEW_LINE


def f_string(string: str, *args: Any, nl: int = 0, **kwargs: Any) -> str:
  """Format style string interpolation.

  :param string: The string to interpolate.
  :param args: The positional arguments for format.
  :param nl: The number of newlines to add to the end of the string.
  :param kwargs: The keyword arguments for format.
  """

  return string.format(*args, **kwargs) + (NEW_LINE * nl)


def initialize() -> gettext.NullTranslations:
  """Initialize localization support."""

  if os.getenv('LANG') is None:
    default_locale = locale.getdefaultlocale()
    os.environ['LANG'] = str(default_locale[0])

  translations = gettext.translation(
      "base",
      os.path.join(os.path.dirname(text_lint.__file__), "locales"),
      fallback=True,
  )

  return translations


f = f_string
_ = initialize().gettext
