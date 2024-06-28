"""LowerCaseEncoder class."""

import json
from typing import Any


class LowerCaseEncoder(json.JSONEncoder):
  """Encode JSON data while converting strings to lower case."""

  def encode(self, o: Any) -> Any:
    value = super().encode(o)
    if isinstance(value, str):
      return value.lower()
    return value
