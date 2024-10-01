"""ResultForest class."""

from typing import TYPE_CHECKING, Dict, Optional, Sequence, Tuple, Union

from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.results import ResultDoesNotExist
from text_lint.sequencers.lookups import LookupsSequencer
from .cursor import ResultTreeCursor

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller
  from text_lint.operations.validators.args.lookup_expression import (
      LookupExpression,
  )
  from .tree import AliasTreeValue, ResultTree

AliasLookupResult = Union[
    str,
    Sequence["AliasLookupResult"],
    Dict[str, "AliasLookupResult"],
]
AliasTreesKey = Union[str, Tuple[str, ...]]


class ResultForest:
  """A composite of TreeResult instances."""

  def __init__(self) -> None:
    self._trees: Dict["AliasTreesKey", "ResultTree"] = {}
    self.cursor = ResultTreeCursor()
    self.lookup_results: AliasLookupResult = []

  def __len__(self) -> int:
    return len(self._trees)

  def add(self, tree: Optional["ResultTree"]) -> None:
    """Add a TreeResult instance to the ForestResults."""

    if tree is not None:
      value = self._hash_tree_value(tree.value)
      if value in self._trees:
        self._trees[value].children += tree.children
      else:
        self._trees[value] = tree

  def get(self, key: "AliasTreeValue") -> "ResultTree":
    """Retrieve a TreeResult instance from the ForestResults."""

    return self._trees[self._hash_tree_value(key)]

  def _hash_tree_value(self, value: "AliasTreeValue") -> "AliasTreesKey":
    if isinstance(value, list):
      return tuple(value)
    return value

  def lookup(
      self,
      controller: "Controller",
      lookup_expression: "LookupExpression",
      requesting_operation_name: str,
  ) -> "AliasLookupResult":
    """Perform a lookup against the ResultForest."""

    if lookup_expression.source.startswith(LOOKUP_STATIC_VALUE_MARKER):
      self.lookup_results = lookup_expression.source[1:]
      return self.lookup_results

    if lookup_expression.source not in self._trees:
      raise ResultDoesNotExist(
          lookup_expression=lookup_expression,
          requesting_operation_name=requesting_operation_name,
      )

    self.cursor.location = [self.get(lookup_expression.source)]
    self.cursor = self.cursor.clone()
    self.lookup_results = [[lookup_expression.source]]

    lookups = LookupsSequencer(lookup_expression, requesting_operation_name)

    for operation in lookups:
      operation.apply(controller.encapsulate_for_lookup())

    return self.lookup_results
