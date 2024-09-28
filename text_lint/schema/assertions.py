"""SchemaAssertions class."""

from typing import TYPE_CHECKING, Dict, List, Type

from text_lint.operations.assertions import (
    AssertSequenceBegins,
    AssertSequenceEnds,
    assertion_registry,
)
from text_lint.schema.bases.section_base import SchemaSectionBase
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )
  from text_lint.schema.bases.section_base import AliasYamlOperation


class SchemaAssertions(SchemaSectionBase["AssertionBase"]):
  """The assertions section of the schema file."""

  operation_classes: Dict[str, Type["AssertionBase"]] = assertion_registry
  entity_name = "assertion"
  automated_section_end_assertion_name = _("Automated End of Sequence")

  msg_fmt_no_nested_assertions = _("No assertions found")

  def hook_load_operation_instances(
      self,
      operation_instances: List["AssertionBase"],
      operation_definitions: List["AliasYamlOperation"],
  ) -> List["AssertionBase"]:
    """Modify the operation instances prior to returning them all."""

    for operation_index, operation_instance in enumerate(operation_instances):
      operation_instance.schema_validator(
          operation_index,
          operation_instances,
          operation_definitions,
          self._schema,
      )

    operation_instances.append(
        AssertSequenceEnds(name=self.automated_section_end_assertion_name)
    )

    return operation_instances

  def hook_create_operation_instance(
      self,
      operation_class: Type["AssertionBase"],
      yaml_definition: "AliasYamlOperation",
  ) -> "AliasYamlOperation":
    """Modify the yaml definition prior to creating each operation instance."""

    if operation_class.operation == AssertSequenceBegins.operation:
      yaml_definition = self._append_nested_yaml_assertions(yaml_definition)

    return yaml_definition

  def _append_nested_yaml_assertions(
      self,
      yaml_definition: "AliasYamlOperation",
  ) -> "AliasYamlOperation":
    if len(yaml_definition["assertions"]) == 0:
      raise self._schema.create_exception(
          description=f(self.msg_fmt_no_nested_assertions, nl=1),
          operation_definition=yaml_definition
      )

    nested_assertion_set = self.load(yaml_definition["assertions"])
    yaml_definition["assertions"] = nested_assertion_set
    return yaml_definition
