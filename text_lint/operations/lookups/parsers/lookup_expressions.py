"""Lookup expression parser."""

from typing import List, Tuple

from text_lint.config import (
    LOOKUP_SENTINEL,
    LOOKUP_SEPERATOR,
    LOOKUP_STATIC_VALUE_MARKER,
)
from text_lint.exceptions.lookups import LookupSyntaxInvalid
from text_lint.exceptions.schema import (
    LookupExpressionInvalid,
    LookupExpressionInvalidSequence,
)
from text_lint.operations.lookups import lookup_registry
from text_lint.operations.lookups.bases.lookup_base import AliasLookupParams
from text_lint.operations.lookups.parsers.lookups import parse_lookup


class ParsedLookup:
  """A parsed lookup operation with its parameters."""

  def __init__(
      self,
      name: str,
      params: "AliasLookupParams",
  ) -> None:
    self.name = name
    self.params = params


LOOKUPS_SENTINEL_VALUE = [ParsedLookup(name=LOOKUP_SENTINEL, params=[])]


def parse_lookup_expression(value: str) -> Tuple[str, List["ParsedLookup"]]:
  """Extract the save ids, lookups and parameters from a lookup expression."""

  if value.startswith(LOOKUP_STATIC_VALUE_MARKER):
    return value, LOOKUPS_SENTINEL_VALUE

  split_value = value.split(LOOKUP_SEPERATOR)
  segments = split_value[1:]

  source = split_value[0]
  lookups: List["ParsedLookup"] = []

  if not segments:
    return source, LOOKUPS_SENTINEL_VALUE

  current_segment = ""
  found_non_positional_lookup = False

  while segments:

    if current_segment:
      current_segment += LOOKUP_SEPERATOR

    current_segment += segments.pop(0)

    try:
      name, params = parse_lookup(current_segment)
      lookups.append(ParsedLookup(name=name, params=params))
      current_segment = ""

      if name not in lookup_registry:
        continue

      if not lookup_registry[name].is_positional:
        found_non_positional_lookup = True
      elif found_non_positional_lookup:
        raise LookupExpressionInvalidSequence(value)

    except LookupSyntaxInvalid:
      pass

  if (value and not lookups) or current_segment:
    raise LookupExpressionInvalid(value)

  return source, lookups
