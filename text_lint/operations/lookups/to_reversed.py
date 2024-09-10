"""ReversedLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupEncoderBase
from .encoders.reversed import ReversedEncoder

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE = """

- name: reversed transformation lookup example
  operation: validate_debug
  saved:
    - example.capture().0.to_reversed()

"""


class ReversedLookup(LookupEncoderBase):
  """ReversedLookup operation for ResultForest instances."""

  encoder_class = ReversedEncoder
  hint = _("reverse the order of a save id")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "reversed"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Reverse the order of the current lookup results."""

    if isinstance(state.results, str):
      state.results = "".join(reversed(list(state.results)))
    else:
      state.results = self.encode(state.results)
