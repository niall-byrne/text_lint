"""SortedLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupEncoderBase
from .encoders.sorted import SortedEncoder

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: sorted transformation lookup example
  operation: validate_debug
  saved:
    - example.capture.0.to_sorted

"""


class SortedLookup(LookupEncoderBase):
  """SortedLookup operation for ResultForest instances."""

  encoder_class = SortedEncoder
  hint = _("sort the saved results")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "sorted"

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Sort the current lookup results."""

    if isinstance(controller.forest.lookup_results, str):
      controller.forest.lookup_results = "".join(
          sorted(list(controller.forest.lookup_results))
      )
    else:
      controller.forest.lookup_results = self.encode(
          controller.forest.lookup_results
      )
