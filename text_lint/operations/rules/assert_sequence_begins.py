"""AssertSequenceBegins class."""

from typing import TYPE_CHECKING, List

from text_lint.operations.rules.bases.rule_base import RuleBase
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller
  from text_lint.schema import AliasYamlOperation, Schema

YAML_EXAMPLE = """

- name: example assert sequence begins rule
  operation: assert_sequence_begins
  count: 3
  rules:
    - name: example assert blank rule
      operation: assert_blank
    - name: example assert regex rule
      operation: assert_regex
      regex: "^([a-z-]+):\\\\s(.+)$\\n"
      save: example
      splits:
        - group: 1
        - character: "-"
        - group: 2

note: set count to 0 to disable the nested sequence of steps.
      set count to -1 to repeat the nested steps until the eof is reached.

"""


class AssertSequenceBegins(RuleBase):
  """Inform the parser to start repeating a list of rules."""

  hint = _("identify a repeating sequence of parser rules")
  operation = "assert_sequence_begins"
  yaml_example = YAML_EXAMPLE

  msg_fmt_unexpected_rules_after_eof_sequence = _(
      "rule #{0} there are unexpected additional rules following "
      "this 'to eof' sequence declaration"
  )

  def __init__(
      self,
      name: str,
      rules: List[RuleBase],
      count: int,
  ) -> None:
    self.count = count
    self.rules = rules
    super().__init__(name, None, None)

  def apply(
      self,
      controller: "Controller",
  ) -> None:
    """Apply the AssertSequenceBegins rule logic."""

    if self.count == -1 or self.count > 0:
      controller.rules.insert(self.rules, self.count)

  def schema_validator(
      self,
      schema_rule_index: int,
      schema_rule_instances: List["RuleBase"],
      schema_rule_definitions: List["AliasYamlOperation"],
      schema: "Schema",
  ) -> None:
    """Optional additional schema level validation for this rule."""

    if (
        self.count == -1
        and schema_rule_index + 1 != len(schema_rule_instances)
    ):
      raise schema.create_exception(
          description=f(
              self.msg_fmt_unexpected_rules_after_eof_sequence,
              schema_rule_index,
              nl=1,
          ),
          operation_definition=self._simplify_yaml_definition(
              schema_rule_definitions[schema_rule_index],
          )
      )

  def _simplify_yaml_definition(
      self,
      schema_rule_definition: "AliasYamlOperation",
  ) -> "AliasYamlOperation":
    schema_rule_definition["rules"] = [
        rule.operation for rule in schema_rule_definition["rules"]
    ]
    return schema_rule_definition
