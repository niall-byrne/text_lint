"""JsonLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.operations.lookups.encoders.tree import ResultTreeEncoder
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupEncoderBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: json result transformation lookup example
  operation: validate_debug
  saved:
    - example.capture.to_json

"""


class JsonLookup(LookupEncoderBase):
  """JsonLookup operation for ResultForest instances."""

  encoder_class = ResultTreeEncoder
  hint = _("create a JSON representation of the saved result")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "json"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Create a JSON representation of the current ResultForest location."""

    controller.forest.lookup_results = self.encode(
        controller.forest.cursor.location
    )
