"""AssertionSequencer class."""

from typing import TYPE_CHECKING

from .bases.operator_base import OperatorBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )
  from text_lint.schema import Schema


class AssertionSequencer(OperatorBase["AssertionBase"]):
  """Iterator that returns parser assertions in the correct sequence."""

  def __init__(self, schema: "Schema") -> None:
    super().__init__(schema.load_assertions())
