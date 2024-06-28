"""ResultForest class."""

from typing import TYPE_CHECKING, Dict, Optional, Sequence, Tuple, Union

from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.results import ResultDoesNotExist
from text_lint.sequencers.lookups import LookupsSequencer
from .cursor import ResultTreeCursor

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter import Linter
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

  def lookup_expression(
      self,
      linter: "Linter",
      lookup_expression: "LookupExpression",
  ) -> "AliasLookupResult":
    """Perform a lookup against the ResultForest."""

    if lookup_expression.source.startswith(LOOKUP_STATIC_VALUE_MARKER):
      return lookup_expression.source[1:]

    try:
      self.get(lookup_expression.source)
    except KeyError as exc:
      raise ResultDoesNotExist(
          lookup_expression=lookup_expression,
          requesting_operation_name=linter.validators.last.name,
      ) from exc

    self.cursor.location = [self.get(lookup_expression.source)]
    self.cursor = self.cursor.clone()
    self.lookup_results = [[lookup_expression.source]]

    lookups = LookupsSequencer(lookup_expression, linter.validators.last.name)

    for operation in lookups:
      operation.apply(linter.states.lookup())

    return self.lookup_results
