"""Version exceptions."""

from typing import Any

from text_lint.utilities.translations import _


class VersionExceptionBase(ValueError):
  """Base class for version exceptions."""


class InvalidVersion(VersionExceptionBase):
  """Raised when a value does not contain a valid version."""

  msg_fmt_invalid = _("The value '{0}' is not a valid version!")

  def __init__(self, invalid_version_value: Any) -> None:
    super().__init__(self.msg_fmt_invalid.format(str(invalid_version_value)))
