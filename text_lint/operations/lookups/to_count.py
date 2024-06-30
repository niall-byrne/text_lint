"""CountLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: count transformation lookup example
  operation: validate_debug
  saved:
    - example.capture.to_count

"""


class CountLookup(LookupBase):
  """CountLookup operation for ResultForest instances."""

  hint = _("convert the saved result to a counted value")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "count"

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Convert the current result set to a counted value."""

    controller.forest.lookup_results = str(
        len(controller.forest.lookup_results)
    )
