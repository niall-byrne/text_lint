"""SchemaSettings class."""

import re
from typing import Optional


class SchemaSettings:
  """Settings embedded in the schema."""

  def __init__(self, comment_regex: Optional[str] = None) -> None:
    """Initialize SchemaSettings instances.

    :param comment_regex: A regular expression used to identify comment lines.
    """
    self.comment_regex = comment_regex
    self.validate()

  def validate(self) -> None:
    """Validate all settings.

    :raises: re.error
    """
    if self.comment_regex:
      re.compile(self.comment_regex, re.DOTALL)
