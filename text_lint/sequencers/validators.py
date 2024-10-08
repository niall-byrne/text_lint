"""ValidatorSequencer class."""

from typing import TYPE_CHECKING

from .bases.operator_base import OperatorBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.validators.bases.validator_base import (
      ValidationBase,
  )
  from text_lint.schema import Schema


class ValidatorSequencer(OperatorBase["ValidationBase"]):
  """Iterator that returns parsing validators in the correct sequence."""

  def __init__(self, schema: "Schema") -> None:
    super().__init__(schema.load_validators())
