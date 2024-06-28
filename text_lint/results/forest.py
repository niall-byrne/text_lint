"""ResultForest class."""

from typing import TYPE_CHECKING, Dict, List, Optional, Union

from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.results import ResultDoesNotExist
from text_lint.sequencers.lookups import LookupsSequencer
from text_lint.utilities.translations import _
from .cursor import ResultTreeCursor

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller
  from text_lint.operations.validators.args.result_set import ResultSet
  from text_lint.results.tree import AliasRecursiveTreeResult
  from .tree import ResultTree

AliasNestedStrings = Union[str, List[str], List[List[str]]]
AliasLookupResult = Union[
    "AliasNestedStrings",
    "AliasRecursiveTreeResult",
]


class ResultForest:
  """A composite of TreeResult instances."""

  msg_fmt_does_not_exist_hint = _(
      'results are created when applying the "rules" section of the schema'
  )

  def __init__(self) -> None:
    self.trees: Dict[str, "ResultTree"] = {}
    self.cursor = ResultTreeCursor()
    self.lookup_results: AliasLookupResult = []

  def add(self, tree: Optional["ResultTree"]) -> None:
    """Add a TreeResult instance to the ForestResults."""

    if tree is not None:
      if tree.value in self.trees:
        self.trees[tree.value].children += tree.children
      else:
        self.trees[tree.value] = tree

  def lookup(
      self,
      controller: "Controller",
      requested_result: "ResultSet",
      requesting_operation_name: str,
  ) -> "AliasLookupResult":
    """Perform a lookup against the ResultForest."""

    if requested_result.source.startswith(LOOKUP_STATIC_VALUE_MARKER):
      self.lookup_results = requested_result.source[1:]
      return self.lookup_results

    if requested_result.source not in self.trees:
      raise ResultDoesNotExist(
          result_set=requested_result,
          requesting_operation_name=requesting_operation_name,
      )

    self.cursor.location = [self.trees[requested_result.source]]
    self.cursor = self.cursor.clone()
    self.lookup_results = [[requested_result.source]]

    lookups = LookupsSequencer(requested_result, requesting_operation_name)

    for operation in lookups:
      operation.apply(controller)

    return self.lookup_results
