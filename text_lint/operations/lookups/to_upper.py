"""UpperLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupEncoderBase
from .encoders.upper import UpperCaseEncoder

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller.states import LookupState

YAML_EXAMPLE = """

- name: uppercase save id transformation lookup example
  operation: validate_debug
  saved:
    - example.capture.to_upper

"""


class UpperLookup(LookupEncoderBase):
  """UpperLookup operation for ResultForest instances."""

  encoder_class = UpperCaseEncoder
  hint = _("convert a save id's values to uppercase")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "upper"

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Convert the current result set to uppercase characters."""

    state.results = self.encode(state.results)
