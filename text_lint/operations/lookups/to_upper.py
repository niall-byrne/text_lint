"""UpperLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupEncoderBase
from .encoders.upper import UpperCaseEncoder

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: uppercase result transformation lookup example
  operation: validate_debug
  saved:
    - example.capture.to_upper

"""


class UpperLookup(LookupEncoderBase):
  """UpperLookup operation for ResultForest instances."""

  encoder_class = UpperCaseEncoder
  hint = _("convert the saved result's values to uppercase")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "upper"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Convert the current result set to uppercase characters."""

    controller.forest.lookup_results = self.encode(
        controller.forest.lookup_results
    )
