"""SchemaAssertions class."""

from typing import TYPE_CHECKING, Dict, List, Type

from text_lint.operations.assertions import (
    AssertSequenceBegins,
    AssertSequenceEnds,
    assertion_registry,
)
from text_lint.schema.bases.section_base import SchemaSectionBase
from text_lint.utilities.translations import _

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

  def hook_load_operation_instances(
      self,
      operation_instances: List["AssertionBase"],
  ) -> List["AssertionBase"]:
    """Modify the operation instances prior to returning them all."""

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
      nested_assertion_set = self.load(yaml_definition["assertions"])
      yaml_definition["assertions"] = nested_assertion_set

    return yaml_definition
