"""LookupBase class."""

import abc
from typing import TYPE_CHECKING, List, Union

from text_lint.exceptions.lookups import LookupFailure
from text_lint.operations.bases.operation_base import OperationBase
from text_lint.operations.mixins.parameter_validation import (
    ParameterValidationMixin,
    validators,
)
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter import states
  from text_lint.operations.validators.args.lookup_expression import (
      LookupExpression,
  )

AliasLookupParams = List[Union[int, str]]


class LookupBase(
    OperationBase["states.LookupState"],
    ParameterValidationMixin,
    abc.ABC,
):
  """Lookup operation base class."""

  is_positional = False

  msg_fmt_invalid_parameters = _("Received invalid parameters: '{0}' !")

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
    self.validate_parameters()

  class Parameters:
    lookup_name = {"type": str}
    lookup_params = {
        "type":
            list,
        "validators": [
            validators.create_is_equal(
                0,
                conversion_function=len,
            ),
        ],
    }

  @abc.abstractmethod
  def apply(
      self,
      state: "states.LookupState",
  ) -> None:
    """Base method for applying a lookup."""

  def validate_parameters(self) -> None:
    try:
      super().validate_parameters()
    except TypeError as exc:
      raise LookupFailure(
          translated_description=f(
              self.msg_fmt_invalid_parameters,
              self.lookup_params,
              nl=1,
          ),
          lookup=self,
      ) from exc
