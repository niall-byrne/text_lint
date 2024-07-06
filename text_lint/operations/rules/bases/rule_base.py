"""RuleBase class."""

import abc
from typing import TYPE_CHECKING, List, Match, Optional

from text_lint.operations.bases.operation_base import OperationBase
from text_lint.operations.rules.args.split import AliasYamlSplit, SplitArgs
from text_lint.results.tree import ResultTree

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller
  from text_lint.schema import AliasYamlOperation, Schema


class RuleBase(OperationBase, abc.ABC):
  """Parser rule base class."""

  matches: List[Match[str]]

  def __init__(
      self,
      name: str,
      save: Optional[str] = None,
      splits: Optional[AliasYamlSplit] = None,
  ) -> None:
    self.name = name
    self.splits = SplitArgs.create(splits)
    self.save = save
    self.matches = []

  @abc.abstractmethod
  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Base method for applying a rule."""

  @property
  def results(self) -> Optional["ResultTree"]:
    """Cache and return results for this rule after it's been applied."""

    if not self.save:
      return None

    result = ResultTree(self.save)

    for match in self.matches:
      result.add_matches(match.groups(), self.splits.as_dict())

    return result

  def schema_validator(
      self,
      schema_rule_index: int,
      schema_rule_instances: List["RuleBase"],
      schema_rule_definitions: List["AliasYamlOperation"],
      schema: "Schema",
  ) -> None:
    """Optional additional schema level validation for this rule."""
