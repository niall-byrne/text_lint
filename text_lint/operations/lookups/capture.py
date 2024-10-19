"""CaptureLookup class."""

from typing import TYPE_CHECKING, List, Union, cast

from text_lint.exceptions.lookups import LookupFailure
from text_lint.operations.bases.operation_base import YAML_EXAMPLE_SECTIONS
from text_lint.operations.mixins.parameter_validation import validators
from text_lint.results.tree import ResultTree
from text_lint.utilities.translations import _, f
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState
  from text_lint.operations.lookups.bases.lookup_base import AliasLookupParams
  from text_lint.operations.validators.args.lookup_expression import (
      LookupExpression,
  )
  from text_lint.results.forest import AliasLookupResult

YAML_EXAMPLE_COMPONENTS = (
    _("capture group lookup example"),
    _("Capture groups are indexed and need a parameter"),
    _("1st regex capture group"),
    _("2nd regex capture group"),
    _("3rd regex capture group"),
)
YAML_EXAMPLE = """

- name: {0}
  operation: validate_debug
  saved:
    - example.capture(1)                      # {2}

{notes_section}:
  - {1}:
    - example.capture(2)                      # {3}
    - example.capture(3)                      # {4}

""".format(*YAML_EXAMPLE_COMPONENTS, **YAML_EXAMPLE_SECTIONS)

AliasRecursiveForestLocation = Union[
    ResultTree,
    List[Union["ResultTree", 'AliasRecursiveForestLocation']],
]


class CaptureLookup(LookupBase):
  """CaptureLookup operation for ResultForest instances."""

  index: int

  hint = _("select the next capture group of a save id")
  is_positional = True
  operation = "capture"
  yaml_example = YAML_EXAMPLE

  msg_fmt_capture_group_not_found = _("Capture group '{0}' not found!")

  def __init__(
      self,
      lookup_name: str,
      lookup_expression: "LookupExpression",
      lookup_params: "AliasLookupParams",
      requesting_operation_name: str,
  ) -> None:
    super().__init__(
        lookup_name,
        lookup_expression,
        lookup_params,
        requesting_operation_name,
    )
    self.index = cast(int, self.lookup_params[0])

  class Parameters(LookupBase.Parameters):
    lookup_params = {
        "type":
            list,
        "of":
            int,
        "validators":
            [
                validators.create_is_equal(
                    1,
                    conversion_function=len,
                ),
                validators.create_is_greater_than_or_equal(
                    1,
                    conversion_function=validators.convert_to_selection(0),
                ),
            ],
    }

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Select a capture group from the current ResultForest location."""

    state.results = []

    while self.index > 0:
      self.index -= 1
      self._update_location(state)

    self._update_results(
        state.cursor.location,
        state.results,
    )

    if not state.results:
      raise self._create_capture_group_not_found()

  def _update_location(
      self,
      state: "LookupState",
  ) -> None:
    state.cursor.increment_depth()

  def _update_results(
      self,
      forest_location: "AliasRecursiveForestLocation",
      thicket: List["AliasLookupResult"],
  ) -> None:
    if isinstance(forest_location, ResultTree):
      thicket += [forest_location.value]
    if isinstance(forest_location, list):
      for grove in forest_location:
        self._update_results(grove, thicket)

  def _create_capture_group_not_found(self) -> LookupFailure:
    return LookupFailure(
        translated_description=f(
            self.msg_fmt_capture_group_not_found,
            self.lookup_params[0],
            nl=1,
        ),
        lookup=self,
    )
