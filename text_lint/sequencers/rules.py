"""RuleSequencer class."""

from typing import TYPE_CHECKING

from .bases.operator_base import OperatorBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.rules.bases.rule_base import RuleBase
  from text_lint.schema import Schema


class RuleSequencer(OperatorBase["RuleBase"]):
  """Iterator that returns parsing rules in the correct sequence."""

  def __init__(self, schema: "Schema") -> None:
    super().__init__(schema.load_rules())
