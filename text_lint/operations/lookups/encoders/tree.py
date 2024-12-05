"""ResultTreeEncoder class."""

import json
from typing import Any

from text_lint.results.tree import ResultTree


class ResultTreeEncoder(json.JSONEncoder):
  """JSON encoder that converts all contained ResultTrees instances."""

  def default(self, o: Any) -> Any:
    """Encode as JSON while converting all contained ResultTree instances.

    :param o: The object being converted.
    :returns: The converted object.
    """
    if isinstance(o, ResultTree):
      return o.representation()
    return super().default(o)
