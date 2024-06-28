"""UniqueEncoder class."""

import json
from typing import Any, List


class UniqueEncoder(json.JSONEncoder):
  """Encode JSON data while ensuring all lists contain unique values."""

  def _recursive_unique_lists(
      self,
      target: Any,
  ) -> Any:
    if isinstance(target, list):
      unique_list: List[Any] = []
      for value in target:
        value = self._recursive_unique_lists(value)
        if value not in unique_list:
          unique_list.append(value)
      return unique_list
    if isinstance(target, dict):
      for key, value in target.copy().items():
        target[key] = self._recursive_unique_lists(value)
    return target

  def encode(self, o: Any) -> Any:
    value = self._recursive_unique_lists(o)
    return super().encode(value)
