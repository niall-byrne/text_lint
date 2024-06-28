"""LookupEncoderBase class."""
import abc
import json
from typing import TYPE_CHECKING, Any, Dict, Type

from .lookup_base import LookupBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.validators.args.result_set import ResultSet


class LookupEncoderBase(LookupBase, abc.ABC):
  """Lookup encoding operation base class."""

  encoder_class: Type[json.JSONEncoder]
  encoder_params: Dict[str, Any]

  def __init__(
      self,
      lookup_name: str,
      result_set: "ResultSet",
      requesting_operation_name: str,
  ) -> None:
    super().__init__(
        lookup_name,
        result_set,
        requesting_operation_name,
    )
    self.encoder_params = {}

  def encode(self, value_set: Any) -> Any:
    return json.loads(
        self.encoder_class(**self.encoder_params).encode(value_set)
    )
