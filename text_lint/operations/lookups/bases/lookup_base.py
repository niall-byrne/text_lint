"""LookupBase class."""

import abc
from typing import TYPE_CHECKING

from text_lint.operations.bases.operation_base import OperationBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import states
  from text_lint.operations.validators.args.lookup_expression import (
      LookupExpression,
  )


class LookupBase(OperationBase["states.LookupState"], abc.ABC):
  """Lookup operation base class."""

  is_positional = False

  def __init__(
      self,
      lookup_name: str,
      lookup_expression: "LookupExpression",
      requesting_operation_name: str,
  ) -> None:
    self.lookup_name = lookup_name
    self.requesting_operation_name = requesting_operation_name
    self.lookup_expression = lookup_expression

  @abc.abstractmethod
  def apply(
      self,
      state: "states.LookupState",
  ) -> None:
    """Base method for applying an assertions."""
