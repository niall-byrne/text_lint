"""SchemaSettings class."""

import re
from typing import Optional


class SchemaSettings:
  """Settings embedded in the schema."""

  def __init__(self, comment_regex: Optional[str] = None) -> None:
    self.comment_regex = comment_regex
    self.validate()

  def validate(self) -> None:
    if self.comment_regex:
      re.compile(self.comment_regex, re.DOTALL)
