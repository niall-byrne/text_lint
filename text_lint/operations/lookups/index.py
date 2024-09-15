"""IndexLookup class."""

from typing import TYPE_CHECKING

from text_lint.exceptions.lookups import LookupFailure
from text_lint.utilities.translations import _, f
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState

YAML_EXAMPLE_COMPONENTS = (
    _("index save id lookup example"),
)
YAML_EXAMPLE = """

- name: {0}
  operation: validate_debug
  saved:
    - example.capture(1).1

""".format(*YAML_EXAMPLE_COMPONENTS)


class IndexLookup(LookupBase):
  """IndexLookup operation for ResultForest instances."""

  hint = _("select a value from a save id by index")
  operation = "index"
  yaml_example = YAML_EXAMPLE

  msg_fmg_invalid_index_description = _("No value at index '{0}' !")

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Select the indexed tree from the current ResultForest location."""

    index = int(self.lookup_name)

    try:
      self._update_location(state, index)
    except IndexError:
      pass

    try:
      self._update_results(state, index)
    except (IndexError, TypeError) as exc:
      raise self._create_lookup_failure() from exc

  def _update_location(self, state: "LookupState", index: int) -> None:
    new_location = state.cursor.location[index]
    if not isinstance(new_location, list):
      new_location = [new_location]
    state.cursor.location = new_location

  def _update_results(self, state: "LookupState", index: int) -> None:
    current_results = state.results
    if isinstance(current_results, (tuple, dict)):
      raise self._create_lookup_failure()
    state.results = current_results[index]

  def _create_lookup_failure(self) -> LookupFailure:
    return LookupFailure(
        translated_description=f(
            self.msg_fmg_invalid_index_description,
            self.lookup_name,
            nl=1,
        ),
        lookup=self,
    )
