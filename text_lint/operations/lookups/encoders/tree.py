"""ResultTreeEncoder class."""

import json
from typing import Any

from text_lint.results.tree import ResultTree


class ResultTreeEncoder(json.JSONEncoder):
  """Encode JSON data containing ResultTrees instances."""

  def default(self, o: Any) -> Any:
    if isinstance(o, ResultTree):
      return o.representation()
    return super().default(o)
