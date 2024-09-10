"""Lookups parser."""

import re
from ast import literal_eval
from typing import Tuple

from text_lint.config import (
    LOOKUP_NAME_REGEX,
    LOOKUP_SENTINEL,
    LOOKUP_STATIC_VALUE_MARKER,
)
from text_lint.exceptions.lookups import LookupSyntaxInvalid
from text_lint.operations.lookups.bases.lookup_base import AliasLookupParams


def parse_lookup(value: str) -> Tuple[str, "AliasLookupParams"]:
  """Extract both a lookup name and it's parameters from a string value."""

  if (
      value == LOOKUP_SENTINEL or value.isdigit()
      or value.startswith(LOOKUP_STATIC_VALUE_MARKER)
  ):
    return value, []

  regex_match = re.match(LOOKUP_NAME_REGEX, value)

  if not regex_match:
    raise LookupSyntaxInvalid(value)

  lookup_name = regex_match.group(1)

  try:
    lookup_params = literal_eval("[" + regex_match.group(2) + "]")
    assert isinstance(lookup_params, list)
    for parameter in lookup_params:
      assert isinstance(parameter, (str, int))
  except (SyntaxError, AssertionError, ValueError) as exc:
    raise LookupSyntaxInvalid(value) from exc

  return lookup_name, lookup_params
