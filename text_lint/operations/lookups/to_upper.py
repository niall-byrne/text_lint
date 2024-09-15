"""UpperLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupEncoderBase
from .encoders.upper import UpperCaseEncoder

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE_COMPONENTS = (
    _("uppercase save id transformation lookup example"),
)
YAML_EXAMPLE = """

- name: {0}
  operation: validate_debug
  saved:
    - example.capture(1).to_upper()

""".format(*YAML_EXAMPLE_COMPONENTS)


class UpperLookup(LookupEncoderBase):
  """UpperLookup operation for ResultForest instances."""

  encoder_class = UpperCaseEncoder
  hint = _("convert a save id's values to uppercase")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "upper"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Convert the current result set to uppercase characters."""

    state.results = self.encode(state.results)
