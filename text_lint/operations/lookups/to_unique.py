"""UniqueLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupEncoderBase
from .encoders.unique import UniqueEncoder

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE = """

- name: unique save id transformation lookup example
  operation: validate_debug
  saved:
    - example.capture().to_unique()

"""


class UniqueLookup(LookupEncoderBase):
  """UniqueLookup operation for ResultForest instances."""

  encoder_class = UniqueEncoder
  hint = _("select only unique values from a save id")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "unique"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Select only unique values from a save id."""

    state.results = self.encode(state.results)
