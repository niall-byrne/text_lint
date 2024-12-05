"""ValidatorSequencer class."""

from typing import TYPE_CHECKING

from text_lint.sequencers.bases.operator_base import OperatorBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.validators.bases.validator_base import (
      ValidatorBase,
  )
  from text_lint.schema import Schema


class ValidatorSequencer(OperatorBase["ValidatorBase"]):
  """Iterator that returns validator operations in the correct sequence."""

  def __init__(self, schema: "Schema") -> None:
    """Initialize ValidatorSequencer instances.

    :param schema: The schema instance to load validator operations from.
    """
    super().__init__(schema.load_validators())
