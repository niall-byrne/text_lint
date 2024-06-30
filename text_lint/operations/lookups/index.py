"""IndexLookup class."""

from typing import TYPE_CHECKING

from text_lint.exceptions.lookups import LookupFailure
from text_lint.utilities.translations import _, f
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller

YAML_EXAMPLE = """

- name: index result lookup example
  operation: validate_debug
  saved:
    - example.capture.1

"""


class IndexLookup(LookupBase):
  """IndexLookup operation for ResultForest instances."""

  hint = _("select an entry from the saved results by index")
  operation = "index"

  msg_fmg_invalid_index_description = _("No value at index '{0}' !")

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Select the indexed tree from the current ResultForest location."""

    index = int(self.lookup_name)

    try:
      self._update_location(controller, index)
      self._update_results(controller, index)
    except (IndexError, TypeError) as exc:
      raise self._create_lookup_failure() from exc

  def _update_location(self, controller: "Controller", index: int) -> None:
    new_location = controller.forest.cursor.location[index]
    if not isinstance(new_location, list):
      new_location = [new_location]
    controller.forest.cursor.location = new_location

  def _update_results(self, controller: "Controller", index: int) -> None:
    current_results = controller.forest.lookup_results
    if isinstance(current_results, (tuple, dict)):
      raise self._create_lookup_failure()
    controller.forest.lookup_results = current_results[index]

  def _create_lookup_failure(self) -> LookupFailure:
    return LookupFailure(
        description=f(
            self.msg_fmg_invalid_index_description,
            self.lookup_name,
            nl=1,
        ),
        lookup=self,
    )
