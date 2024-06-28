"""LookupsSequencer class."""

from typing import TYPE_CHECKING

from text_lint.operations.lookups import lookup_registry
from .bases.operator_base import OperatorBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.lookups.bases.lookup_base import LookupBase
  from text_lint.operations.validators.args.result_set import ResultSet


class LookupsSequencer(OperatorBase["LookupBase"]):
  """Iterator that returns ResultForest lookups in the correct sequence."""

  def __init__(
      self,
      result_set: "ResultSet",
      requesting_operation_name: str,
  ) -> None:
    instances = [
        lookup_registry[lookup](
            lookup,
            result_set,
            requesting_operation_name,
        ) for lookup in result_set.lookups
    ]
    super().__init__(instances)
