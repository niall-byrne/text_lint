"""LowerCaseEncoder class."""

import json
from typing import Any


class LowerCaseEncoder(json.JSONEncoder):
  """JSON encoder that converts strings to lower case."""

  def encode(self, o: Any) -> Any:
    """Encode as JSON while converting all strings values to lower case.

    :param o: The object being converted.
    :returns: The converted object.
    """
    value = super().encode(o)
    if isinstance(value, str):
      return value.lower()
    return value
