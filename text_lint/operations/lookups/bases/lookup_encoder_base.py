"""LookupEncoderBase class."""
import abc
import json
from typing import TYPE_CHECKING, Any, Dict, Type

from .lookup_base import AliasLookupParams, LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.validators.args.lookup_expression import (
      LookupExpression,
  )


class LookupEncoderBase(LookupBase, abc.ABC):
  """Lookup result encoding operation base class."""

  encoder_class: Type[json.JSONEncoder]
  encoder_params: Dict[str, Any]

  def __init__(
      self,
      lookup_name: str,
      lookup_expression: "LookupExpression",
      lookup_params: "AliasLookupParams",
      requesting_operation_name: str,
  ) -> None:
    super().__init__(
        lookup_name,
        lookup_expression,
        lookup_params,
        requesting_operation_name,
    )
    self.encoder_params = {}

  def encode(self, value_set: Any) -> Any:
    return json.loads(
        self.encoder_class(**self.encoder_params).encode(value_set)
    )
