"""UpperCaseEncoder class."""

import json
from typing import Any


class UpperCaseEncoder(json.JSONEncoder):
  """Encode JSON data while converting strings to upper case."""

  def encode(self, o: Any) -> Any:
    value = super().encode(o)
    if isinstance(value, str):
      return value.upper()
    return value
