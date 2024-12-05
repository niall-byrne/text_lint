"""UpperCaseEncoder class."""

import json
from typing import Any


class UpperCaseEncoder(json.JSONEncoder):
  """JSON encoder that converts strings to upper case."""

  def encode(self, o: Any) -> Any:
    """Encode as JSON while converting all strings values to upper case.

    :param o: The object being converted.
    :returns: The converted object.
    """
    value = super().encode(o)
    if isinstance(value, str):
      return value.upper()
    return value
