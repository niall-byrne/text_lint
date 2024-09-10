"""LookupBase class."""

import abc
from typing import TYPE_CHECKING, List, Union

from text_lint.exceptions.lookups import LookupFailure
from text_lint.operations.bases.operation_base import OperationBase
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter import states
  from text_lint.operations.validators.args.lookup_expression import (
      LookupExpression,
  )

AliasLookupParams = List[Union[int, str]]


class LookupBase(OperationBase["states.LookupState"], abc.ABC):
  """Lookup operation base class."""

  is_positional = False

  msg_fmt_unexpected_parameters = _("Received unexpected parameters: '{0}' !")

  def __init__(
      self,
      lookup_name: str,
      lookup_expression: "LookupExpression",
      lookup_params: "AliasLookupParams",
      requesting_operation_name: str,
  ) -> None:
    self.lookup_name = lookup_name
    self.lookup_expression = lookup_expression
    self.lookup_params = lookup_params
    self.requesting_operation_name = requesting_operation_name
    self.validate_params()

  def validate_params(self) -> None:
    """Override to perform validation on the lookup parameters."""
    if self.lookup_params:
      raise LookupFailure(
          translated_description=f(
              self.msg_fmt_unexpected_parameters,
              self.lookup_params,
              nl=1,
          ),
          lookup=self,
      )

  @abc.abstractmethod
  def apply(
      self,
      state: "states.LookupState",
  ) -> None:
    """Base method for applying an assertions."""
