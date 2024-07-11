"""Lookup expression YAML argument definitions."""
from typing import Dict, Iterator, List, Optional

from text_lint.config import LOOKUP_SENTINEL, LOOKUP_SEPERATOR
from text_lint.operations.lookups import lookup_registry
from text_lint.utilities.translations import _

AliasYamlLookupExpressionSet = List[str]
AliasResultOptions = Dict[str, Optional["AliasResultOptions"]]


class LookupExpressionSetArg:
  """"A set of YAML argument definitions for lookup expressions."""

  msg_fmt_invalid_lookup_expression_set = _(
      "The value '{0}' is not a valid set of lookup expressions"
  )

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

      if not isinstance(yaml_input, (list, tuple)):
        raise TypeError(
            cls.msg_fmt_invalid_lookup_expression_set.format(yaml_input)
        )

    return cls(lookup_expression_set=created_set)


class LookupExpression:
  """A lookup expression definition."""

  lookups: List[str]
  name: str
  source: str

  def __init__(
      self,
      lookup_expression: str,
  ) -> None:
    self.name = lookup_expression
    self._parsing_container: List[str] = lookup_expression.split(
        LOOKUP_SEPERATOR
    )
    self.source = self._parsing_container[0]
    self.lookups = self._parsing_container[1:]
    if len(self.lookups) == 0:
      self.lookups = [LOOKUP_SENTINEL]
    self.validate_lookups()

  def validate_lookups(self) -> None:
    found_non_positional_lookup = False
    for lookup in self.lookups:

      if lookup not in lookup_registry:
        continue

      if not lookup_registry[lookup].is_positional:
        found_non_positional_lookup = True
      elif found_non_positional_lookup:
        raise ValueError(
            "Transformations belong at the end of a lookup expression."
        )
