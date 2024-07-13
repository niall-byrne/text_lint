"""ReversedEncoder class."""

import json
from typing import Any, Dict


class ReversedEncoder(json.JSONEncoder):
  """Encode JSON data while reversing dictionaries, lists and tuples."""

  def _recursive_reversed(
      self,
      target: Any,
  ) -> Any:
    if isinstance(target, (list, tuple)):
      target = list(
          reversed([self._recursive_reversed(element) for element in target])
      )
    if isinstance(target, dict):
      new_dictionary: Dict[Any, Any] = {}
      for key in reversed(target.keys()):
        new_dictionary[key] = self._recursive_reversed(target[key])
      target = new_dictionary
    return target

  def encode(self, o: Any) -> Any:
    value = self._recursive_reversed(o)
    return super().encode(value)
