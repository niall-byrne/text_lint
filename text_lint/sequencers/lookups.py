"""LookupsSequencer class."""

from typing import TYPE_CHECKING

from text_lint.operations.lookups import lookup_registry
from text_lint.sequencers.bases.operator_base import OperatorBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.lookups.bases.lookup_base import LookupBase
  from text_lint.operations.validators.args.lookup_expression import (
      LookupExpression,
  )


class LookupsSequencer(OperatorBase["LookupBase"]):
  """Iterator that returns ResultForest lookups in the correct sequence."""

  def __init__(
      self,
      lookup_expression: "LookupExpression",
      requesting_operation_name: str,
  ) -> None:
    """Initialize LookupsSequencer instances.

    :param lookup_expression: The lookup expression being evaluated.
    :param requesting_operation_name: The validator for this lookup expression.
    """
    instances = [
        lookup_registry[lookup.name](
            lookup.name,
            lookup_expression,
            lookup.params,
            requesting_operation_name,
        ) for lookup in lookup_expression.lookups
    ]
    super().__init__(instances)
