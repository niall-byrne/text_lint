"""SortedEncoder class."""

import json
from typing import Any, List


class SortedEncoder(json.JSONEncoder):
  """Encode JSON data while sorting dictionaries, lists and tuples."""

  def encode(self, o: Any) -> Any:
    value = self._recursive_sorted(o)
    return super().encode(value)

  def _recursive_sorted(
      self,
      target: Any,
  ) -> Any:
    if isinstance(target, (list, tuple)):
      string_elements: List[str] = []
      other_elements: List[Any] = []
      for element in target:
        if isinstance(element, str):
          string_elements.append(element)
        else:
          other_elements.append(element)
      target = sorted(string_elements) + [
          self._recursive_sorted(element) for element in other_elements
      ]
    if isinstance(target, dict):
      for key, value in target.items():
        target[key] = self._recursive_sorted(value)
      target = dict(sorted(
          target.items(),
          key=lambda item: str(item[1]),
      ))
    return target
