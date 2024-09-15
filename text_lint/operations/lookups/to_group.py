"""GroupLookup class."""

from itertools import chain
from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE_COMPONENTS = (
    _("group lookup example"),
)
YAML_EXAMPLE = """

- name: {0}
  operation: validate_debug
  saved:
    - example.capture(1).to_group()

""".format(*YAML_EXAMPLE_COMPONENTS)


class GroupLookup(LookupBase):
  """GroupLookup operation for ResultForest instances."""

  hint = _("group the values of a save id")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "group"
  yaml_example = YAML_EXAMPLE

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Group the current result set into a flat list."""

    state.results = list(chain.from_iterable(state.results))
