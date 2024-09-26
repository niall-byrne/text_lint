"""AssertionBase class."""

import abc
import re
from typing import TYPE_CHECKING, List, Match, Optional, Sequence

from text_lint.config import SAVED_NAME_REGEX
from text_lint.exceptions.assertions import AssertionCaptureGroupNotFound
from text_lint.exceptions.results import SplitGroupNotFound
from text_lint.exceptions.schema import SaveIdInvalid
from text_lint.operations.assertions.args.split import (
    AliasYamlSplit,
    SplitArgs,
)
from text_lint.operations.bases.operation_base import OperationBase
from text_lint.results.tree import ResultTree

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter import states
  from text_lint.schema import AliasYamlOperation, Schema


class AssertionBase(OperationBase["states.AssertionState"], abc.ABC):
  """Assertion operation base class."""

  def __init__(
      self,
      name: str,
      save: Optional[str] = None,
      splits: Optional[AliasYamlSplit] = None,
  ) -> None:
    self.name = name
    self.save = save
    self.__save_validator()
    self.splits = SplitArgs.create(splits)

  @abc.abstractmethod
  def apply(self, state: "states.AssertionState") -> None:
    """Assertion implementation"""

  def create_result_tree(
      self,
      matches: Sequence[Match[str]],
  ) -> Optional["ResultTree"]:
    """Return a result tree for any matches this assertion generates."""

    if not self.save:
      return None

    result = ResultTree(self.save)

    for match in matches:
      try:
        result.add_matches(match.groups(), self.splits.as_dict())
      except SplitGroupNotFound as exc:
        raise AssertionCaptureGroupNotFound(
            assertion=self,
            capture_group=exc.group,
        ) from exc

    return result

  def __save_validator(self) -> None:
    if self.save and not re.match(SAVED_NAME_REGEX, self.save):
      raise SaveIdInvalid(self.save)

  def schema_validator(
      self,
      schema_assertion_index: int,
      schema_assertion_instances: List["AssertionBase"],
      schema_assertion_definitions: List["AliasYamlOperation"],
      schema: "Schema",
  ) -> None:
    """Optional additional schema level validation for this assertion."""
