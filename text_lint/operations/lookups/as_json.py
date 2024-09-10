"""JsonLookup class."""

from typing import TYPE_CHECKING

from text_lint.operations.lookups.encoders.tree import ResultTreeEncoder
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupEncoderBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE = """

- name: save id as json representation example
  operation: validate_debug
  saved:
    - example.capture(1).to_json()

note: This lookup is intended to help debug capture groups in complex loops.

"""


class JsonLookup(LookupEncoderBase):
  """JsonLookup operation for ResultForest instances."""

  encoder_class = ResultTreeEncoder
  hint = _("create a JSON representation of a save id")
  is_positional = True
  operation = "as_json"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Create a JSON representation of the current ResultForest location."""

    state.results = self.encode(state.cursor.location)
