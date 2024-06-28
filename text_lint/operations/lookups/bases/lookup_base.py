"""LookupBase class."""

import abc
from typing import TYPE_CHECKING

from text_lint.operations.bases.operation_base import OperationBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller
  from text_lint.operations.validators.args.result_set import ResultSet


class LookupBase(OperationBase, abc.ABC):
  """Lookup operation base class."""

  is_positional = False

  def __init__(
      self,
      lookup_name: str,
      result_set: "ResultSet",
      requesting_operation_name: str,
  ) -> None:
    self.lookup_name = lookup_name
    self.requesting_operation_name = requesting_operation_name
    self.result_set = result_set

  @abc.abstractmethod
  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Base method for applying an assertions."""
