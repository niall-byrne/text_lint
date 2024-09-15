"""CaptureLookup class."""

from typing import TYPE_CHECKING, List, Union

from text_lint.exceptions.lookups import LookupFailure
from text_lint.operations.bases.operation_base import YAML_EXAMPLE_SECTIONS
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

  msg_fmg_invalid_capture_group = _("Invalid capture group '{0}' !")
  msg_fmg_invalid_parameters = _("Invalid lookup parameters!")

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
    self.index = self._parse_capture_group()

  def validate_params(self) -> None:
    if len(self.lookup_params) != 1:
      raise LookupFailure(
          translated_description=f(
              self.msg_fmg_invalid_parameters,
              [],
              nl=1,
          ),
          lookup=self,
      )

  def _parse_capture_group(self) -> int:
    try:
      assert isinstance(self.lookup_params[0], int)
      index = self.lookup_params[0]
      assert index > 0
      return index
    except AssertionError as exc:
      raise LookupFailure(
          translated_description=f(
              self.msg_fmg_invalid_capture_group,
              self.lookup_params[0],
              nl=1,
          ),
          lookup=self,
      ) from exc

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
      raise self._create_lookup_failure()

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

  def _create_lookup_failure(self) -> LookupFailure:
    return LookupFailure(
        translated_description=f(
            self.msg_fmg_invalid_capture_group,
            self.lookup_params[0],
            nl=1,
        ),
        lookup=self,
    )
