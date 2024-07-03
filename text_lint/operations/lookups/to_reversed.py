"""ReversedLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupEncoderBase
from .encoders.reversed import ReversedEncoder

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: reversed transformation lookup example
  operation: validate_debug
  saved:
    - example.capture.0.to_reversed

"""


class ReversedLookup(LookupEncoderBase):
  """ReversedLookup operation for ResultForest instances."""

  encoder_class = ReversedEncoder
  hint = _("reverse the order of the saved results")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "reversed"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Reverse the order of the current lookup results."""

    if isinstance(controller.forest.lookup_results, str):
      controller.forest.lookup_results = "".join(
          reversed(list(controller.forest.lookup_results))
      )
    else:
      controller.forest.lookup_results = self.encode(
          controller.forest.lookup_results
      )
