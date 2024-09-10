"""SortedLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupEncoderBase
from .encoders.sorted import SortedEncoder

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE = """

- name: sorted transformation lookup example
  operation: validate_debug
  saved:
    - example.capture().0.to_sorted()

"""


class SortedLookup(LookupEncoderBase):
  """SortedLookup operation for ResultForest instances."""

  encoder_class = SortedEncoder
  hint = _("sort the values of a save id")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "sorted"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Sort the current lookup results."""

    if isinstance(state.results, str):
      state.results = "".join(sorted(list(state.results)))
    else:
      state.results = self.encode(state.results)
