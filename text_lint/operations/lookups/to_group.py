"""GroupLookup class."""

from itertools import chain
from typing import TYPE_CHECKING

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.utilities.translations import _
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE = """

- name: group lookup example
  operation: validate_debug
  saved:
    - example.capture().to_group()

"""


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
