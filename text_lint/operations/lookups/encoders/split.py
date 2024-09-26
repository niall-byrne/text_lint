"""SplitEncoder class."""

import json
from typing import Any, List, Optional


class SplitEncoder(json.JSONEncoder):
  """Encode JSON data while splitting strings with a seperator."""

  def __init__(
      self,
      *args: Any,
      seperator: Optional[str] = None,
      **kwargs: Any,
  ) -> None:
    super().__init__(*args, **kwargs)
    self.seperator = seperator

  def encode(self, o: Any) -> Any:
    value = self._recursive_split(o)
    return super().encode(value)

  def _recursive_split(
      self,
      target: Any,
  ) -> Any:
    if isinstance(target, str):
      return target.split(self.seperator)
    if isinstance(target, (list, tuple)):
      split_list: List[Any] = []
      for value in target:
        value = self._recursive_split(value)
        split_list.append(value)
      return split_list
    if isinstance(target, dict):
      for key, value in target.copy().items():
        target[key] = self._recursive_split(value)
    return target
