"""CountLookup class."""

from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_encoder_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE_COMPONENTS = (
    _("count transformation lookup example"),
)
YAML_EXAMPLE = """

- name: {0}
  operation: validate_debug
  saved:
    - example.capture(1).to_count()

""".format(*YAML_EXAMPLE_COMPONENTS)


class CountLookup(LookupBase):
  """CountLookup operation for ResultForest instances."""

  hint = _("transform a save id into a count of values")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "count"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Convert the current result set to a counted value."""

    state.results = str(len(state.results))
