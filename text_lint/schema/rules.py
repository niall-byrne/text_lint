"""SchemaRules class."""

from typing import TYPE_CHECKING, Dict, List, Type

from text_lint.operations.rules import (
    AssertSequenceBegins,
    AssertSequenceEnds,
    rule_registry,
)
from text_lint.schema.bases.section_base import SchemaSectionBase
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.rules.bases.rule_base import RuleBase
  from text_lint.schema.bases.section_base import AliasYamlOperation


class SchemaRules(SchemaSectionBase["RuleBase"]):
  """The rules section of the schema file."""

  operation_classes: Dict[str, Type["RuleBase"]] = rule_registry
  entity_name = "rule"
  automated_section_end_rule_name = _("Automated End of Section")

  def hook_load_operation_instances(
      self,
      operation_instances: List["RuleBase"],
      operation_definitions: List["AliasYamlOperation"],
  ) -> List["RuleBase"]:
    """Modify the operation instances prior to returning them all."""

    for operation_index, operation_instance in enumerate(operation_instances):
      operation_instance.schema_validator(
          operation_index,
          operation_instances,
          operation_definitions,
          self._schema,
      )

    operation_instances.append(
        AssertSequenceEnds(name=self.automated_section_end_rule_name)
    )

    return operation_instances

  def hook_create_operation_instance(
      self,
      operation_class: Type["RuleBase"],
      yaml_definition: "AliasYamlOperation",
  ) -> "AliasYamlOperation":
    """Modify the yaml definition prior to creating each operation instance."""

    if operation_class.operation == AssertSequenceBegins.operation:
      yaml_definition = self._append_nested_yaml_rules(yaml_definition)

    return yaml_definition

  def _append_nested_yaml_rules(
      self,
      yaml_definition: "AliasYamlOperation",
  ) -> "AliasYamlOperation":
    nested_rule_set = self.load(yaml_definition["rules"])
    yaml_definition["rules"] = nested_rule_set
    return yaml_definition
