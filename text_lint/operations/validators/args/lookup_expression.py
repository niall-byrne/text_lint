"""Lookup expression YAML argument definitions."""

from typing import Dict, Iterator, List, Optional

from text_lint.operations.lookups.parsers.lookup_expressions import (
    ParsedLookup,
    parse_lookup_expression,
)

AliasYamlLookupExpressionSet = List[str]
AliasResultOptions = Dict[str, Optional["AliasResultOptions"]]


class LookupExpressionSetArg:
  """"A set of YAML argument definitions for lookup expressions."""

  def __init__(self, lookup_expression_set: List["LookupExpression"]) -> None:
    self._lookup_expression_set = lookup_expression_set

  def __iter__(self) -> Iterator["LookupExpression"]:
    return iter(self._lookup_expression_set)

  def __len__(self) -> int:
    return len(self._lookup_expression_set)

  @classmethod
  def create(
      cls, yaml_input: AliasYamlLookupExpressionSet
  ) -> "LookupExpressionSetArg":
    """Create an instance from YAML input."""

    created_set = []
    for yaml_set in yaml_input:
      created_set.append(LookupExpression(yaml_set))
    return cls(lookup_expression_set=created_set)


class LookupExpression:
  """A lookup expression definition."""

  lookups: List[ParsedLookup]
  name: str
  source: str

  def __init__(
      self,
      lookup_expression: str,
  ) -> None:
    self.name = lookup_expression
    self.source, self.lookups = parse_lookup_expression(lookup_expression)
