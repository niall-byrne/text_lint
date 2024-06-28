"""SchemaSectionBase class."""

import re
from typing import TYPE_CHECKING, Any, Dict, Generic, List, Type, TypeVar

from text_lint.exceptions.schema import SplitGroupInvalid
from text_lint.operations.bases.operation_base import OperationBase
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.schema import Schema

AliasYamlOperation = Dict[str, Any]
TypeOperation = TypeVar("TypeOperation", bound=OperationBase)


class SchemaSectionBase(Generic[TypeOperation]):
  """A section of the schema file containing operation definitions."""

  operation_classes: Dict[str, Type["TypeOperation"]]
  entity_name: "str"

  msg_fmt_invalid_regex = _("{0} #{1} Invalid regex")
  msg_fmt_invalid_split_group = _("{0} #{1} Invalid split group")
  msg_fmt_unknown_operation = _("{0} #{1} Unknown operation")
  msg_fmt_unknown_syntax = _("{0} #{1} Unknown syntax")

  def __init__(self, schema: "Schema") -> None:
    self._schema = schema

  def load(
      self,
      source: List[AliasYamlOperation],
  ) -> List["TypeOperation"]:
    """Load the operation instances from the schema."""

    operation_instances: List["TypeOperation"] = []

    for operation_index, operation_definition in enumerate(source):
      operation_instance = self._parse_schema_instances(
          operation_definition,
          operation_index,
      )
      operation_instances.append(operation_instance)

    operation_instances = self.hook_load_operation_instances(
        operation_instances
    )
    return operation_instances

  def _parse_schema_instances(
      self,
      operation_definition: Dict[str, Any],
      operation_index: int,
  ) -> "TypeOperation":
    try:
      linter_operation = operation_definition["operation"]
      try:
        operation_class = self.operation_classes[linter_operation]
        operation_definition = self.hook_create_operation_instance(
            operation_class,
            operation_definition,
        )
      except KeyError as exc:
        raise self._schema.create_exception(
            description=f(
                self.msg_fmt_unknown_operation,
                self.entity_name,
                operation_index + 1,
                nl=1,
            ),
            operation_definition=operation_definition,
        ) from exc
      del operation_definition["operation"]
      return operation_class(**operation_definition)
    except (AttributeError, TypeError, KeyError) as exc:
      raise self._schema.create_exception(
          description=f(
              self.msg_fmt_unknown_syntax,
              self.entity_name,
              operation_index + 1,
              nl=1,
          ),
          operation_definition=operation_definition,
      ) from exc
    except re.error as exc:
      raise self._schema.create_exception(
          description=f(
              self.msg_fmt_invalid_regex,
              self.entity_name,
              operation_index + 1,
              nl=1,
          ),
          operation_definition=operation_definition,
      ) from exc
    except SplitGroupInvalid as exc:
      raise self._schema.create_exception(
          description=f(
              self.msg_fmt_invalid_split_group,
              self.entity_name,
              operation_index + 1,
              nl=1,
          ),
          operation_definition=operation_definition,
      ) from exc

  def hook_load_operation_instances(
      self,
      operation_instances: List["TypeOperation"],
  ) -> List["TypeOperation"]:
    """Modify the operation instances prior to returning loaded results."""

    return operation_instances

  # pylint: disable=unused-argument
  def hook_create_operation_instance(
      self,
      operation_class: Type["TypeOperation"],
      yaml_definition: "AliasYamlOperation",
  ) -> "AliasYamlOperation":
    """Modify the yaml definition prior to creating the operation instance."""

    return yaml_definition
