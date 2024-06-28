"""NameLookup class."""

from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union

from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.lookups import LookupFailure, LookupUnknown
from text_lint.results.tree import ResultTree
from text_lint.utilities.translations import _, f
from .bases.lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller
  from text_lint.results.cursor import AliasResultForestCursor
  from text_lint.results.forest import AliasLookupResult

YAML_EXAMPLE = """

- name: static value lookup example
  operation: validate_debug
  saved:
    - example.capture.to_group.~static_value
    - ~static_value

note: A static value can be used in the source position of a lookup expression.

"""


class NameLookup(LookupBase):
  """NameLookup operation for ResultForest instances."""

  hint = _("select a static value from a save id")
  operation = "name"

  msg_fmt_failure_description = _("Could not find the specified value.")

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Select the specified tree from the current ResultForest location."""

    if not self.lookup_name.startswith(LOOKUP_STATIC_VALUE_MARKER):
      raise LookupUnknown(lookup=self)

    search_string = self.lookup_name[len(LOOKUP_STATIC_VALUE_MARKER):]

    controller.forest.cursor.flatten()

    self._update_location(controller, search_string)
    self._update_results(controller, search_string)

  def _update_location(
      self,
      controller: "Controller",
      search_string: str,
  ) -> None:
    matches: "AliasResultForestCursor" = []
    self._find_matching_result_tree(
        controller.forest.cursor.location,
        search_string,
        matches,
    )
    if matches:
      controller.forest.cursor.location = matches

  def _find_matching_result_tree(
      self,
      location: Union[ResultTree, "AliasResultForestCursor"],
      search_string: str,
      matches: "AliasResultForestCursor",
  ) -> None:
    if isinstance(location, ResultTree):
      if isinstance(location.value, str):
        if search_string == location.value:
          matches.append(location)
      if isinstance(location.value, list):
        if search_string in location.value:
          matches.append(location)
    else:
      for nested_tree in location:
        self._find_matching_result_tree(
            nested_tree,
            search_string,
            matches,
        )

  def _update_results(
      self,
      controller: "Controller",
      search_string: str,
  ) -> None:
    matches = self._find_matching_result(
        controller.forest.lookup_results,
        search_string,
    )
    if not matches:
      raise self._create_lookup_failure()
    controller.forest.lookup_results = matches

  def _find_matching_result(
      self,
      result: "AliasLookupResult",
      search_string: str,
  ) -> Optional["AliasLookupResult"]:
    if isinstance(result, str):
      if search_string == result:
        return result
    if isinstance(result, (list, tuple)):
      return self._find_match_result_in_iterable(result, search_string)
    if isinstance(result, dict):
      return self._find_match_result_in_dict(
          result,
          search_string,
      )
    return None

  def _find_match_result_in_iterable(
      self,
      result: Union[Tuple["AliasLookupResult", ...], List["AliasLookupResult"]],
      search_string: str,
  ) -> Optional["AliasLookupResult"]:
    if search_string in result:
      return result
    matches = [
        filtered_value for filtered_value in [
            self._find_matching_result(
                nested_result,
                search_string,
            ) for nested_result in result
        ] if filtered_value
    ]
    if matches:
      return matches
    return None

  def _find_match_result_in_dict(
      self,
      result: Dict[str, "AliasLookupResult"],
      search_string: str,
  ) -> Optional["AliasLookupResult"]:
    if search_string in result.keys():
      return result
    for value in result.values():
      if search_string in value:
        return value
    return None

  def _create_lookup_failure(self) -> LookupFailure:
    return LookupFailure(
        description=f(
            self.msg_fmt_failure_description,
            nl=1,
        ),
        lookup=self,
    )
