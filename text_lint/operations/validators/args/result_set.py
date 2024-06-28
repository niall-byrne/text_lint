"""Parser result set YAML argument definitions."""
from typing import Dict, Iterator, List, Optional

from text_lint.config import LOOKUP_SENTINEL, LOOKUP_SEPERATOR
from text_lint.operations.lookups import lookup_registry

AliasYamlResultSet = List[str]
AliasYamlResultDefinition = Dict[str, "AliasYamlResultDefinition"]
AliasResultOptions = Dict[str, Optional["AliasResultOptions"]]


class ResultSetArg:
  """"Parser result set YAML argument definitions."""

  def __init__(self, saved_result_set: List["ResultSet"]) -> None:
    self._saved_result_set = saved_result_set

  def __iter__(self) -> Iterator["ResultSet"]:
    return iter(self._saved_result_set)

  @classmethod
  def create(cls, yaml_input: AliasYamlResultSet) -> "ResultSetArg":
    """Create an instance from YAML input."""

    created_sets = []
    for yaml_set in yaml_input:
      created_sets.append(ResultSet(yaml_set))
    return cls(saved_result_set=created_sets)


class ResultSet:
  """Parser result set definition."""

  lookups: List[str]
  name: str
  source: str

  def __init__(
      self,
      result_lookup_definition: str,
  ) -> None:
    self.name = result_lookup_definition
    self._parsing_container: List[str] = result_lookup_definition.split(
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
