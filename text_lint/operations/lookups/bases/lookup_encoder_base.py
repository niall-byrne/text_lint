"""LookupEncoderBase class."""
import abc
import json
from typing import Any, Type

from .lookup_base import LookupBase


class LookupEncoderBase(LookupBase, abc.ABC):
  """Lookup encoding operation base class."""

  encoder_class: Type[json.JSONEncoder]

  def encode(self, value_set: Any) -> Any:
    return json.loads(json.dumps(
        value_set,
        cls=self.encoder_class,
    ))
