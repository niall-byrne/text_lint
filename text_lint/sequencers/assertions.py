"""AssertionSequencer class."""

from typing import TYPE_CHECKING

from text_lint.sequencers.bases.operator_base import OperatorBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )
  from text_lint.schema import Schema


class AssertionSequencer(OperatorBase["AssertionBase"]):
  """Iterator that returns assertion operations in the correct sequence."""

  def __init__(self, schema: "Schema") -> None:
    """Initialize AssertionSequencer instances.

    :param schema: The schema instance to load assertion operations from.
    """
    super().__init__(schema.load_assertions())
