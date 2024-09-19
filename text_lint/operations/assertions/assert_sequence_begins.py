"""AssertSequenceBegins class."""

from typing import TYPE_CHECKING, List

from text_lint.config import LOOP_COUNT
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.bases.operation_base import YAML_EXAMPLE_SECTIONS
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import AssertionState
  from text_lint.schema import AliasYamlOperation, Schema

YAML_EXAMPLE_COMPONENTS = (
    _("example assert sequence begins assertion"),
    _("example assert blank assertion"),
    _("example assert regex assertion"),
    _("Set count to 0 to disable the nested assertions."),
    _("Set count to {LOOP_COUNT} to repeat the nested assertions until EOF."),
)
YAML_EXAMPLE = """

- name: {0}
  operation: assert_sequence_begins
  count: 3
  assertions:
    - name: {1}
      operation: assert_blank
    - name: {2}
      operation: assert_regex
      regex: "^([a-z-]+):\\\\s(.+)$"
      save: example
      splits:
        - group: 1
        - character: "-"
        - group: 2

{notes_section}:
  - {3}
  - {4}

""".format(
    *YAML_EXAMPLE_COMPONENTS,
    **YAML_EXAMPLE_SECTIONS,
)


class AssertSequenceBegins(AssertionBase):
  """Inform the linter to start repeating a list of assertions."""

  hint = _("identify a repeating sequence of assertions")
  operation = "assert_sequence_begins"
  yaml_example = YAML_EXAMPLE.format(LOOP_COUNT=LOOP_COUNT)

  msg_fmt_invalid_sequence_count = _(
      "assertion #{0} there is an invalid sequence count"
  )
  msg_fmt_unexpected_assertions_after_eof_sequence = _(
      "assertion #{0} there are unexpected additional assertions following "
      "this 'to eof' sequence declaration"
  )

  def __init__(
      self,
      name: str,
      assertions: List[AssertionBase],
      count: int,
  ) -> None:
    self.count = count
    self.assertions = assertions
    super().__init__(name, None, None)

  def apply(
      self,
      state: "AssertionState",
  ) -> None:
    """Apply the AssertSequenceBegins assertion logic."""

    state.loop(self.assertions, self.count)

  def schema_validator(
      self,
      schema_assertion_index: int,
      schema_assertion_instances: List["AssertionBase"],
      schema_assertion_definitions: List["AliasYamlOperation"],
      schema: "Schema",
  ) -> None:
    """Optional additional schema level validation for this assertion."""

    if self.count != LOOP_COUNT and self.count < 0:
      raise schema.create_exception(
          description=f(
              self.msg_fmt_invalid_sequence_count,
              schema_assertion_index,
              nl=1,
          ),
          operation_definition=self._simplify_yaml_definition(
              schema_assertion_definitions[schema_assertion_index],
          )
      )

    if (
        self.count == LOOP_COUNT
        and schema_assertion_index + 1 != len(schema_assertion_instances)
    ):
      raise schema.create_exception(
          description=f(
              self.msg_fmt_unexpected_assertions_after_eof_sequence,
              schema_assertion_index,
              nl=1,
          ),
          operation_definition=self._simplify_yaml_definition(
              schema_assertion_definitions[schema_assertion_index],
          )
      )

  def _simplify_yaml_definition(
      self,
      schema_assertion_definition: "AliasYamlOperation",
  ) -> "AliasYamlOperation":
    schema_assertion_definition["assertions"] = [
        assertion.operation
        for assertion in schema_assertion_definition["assertions"]
    ]
    return schema_assertion_definition
