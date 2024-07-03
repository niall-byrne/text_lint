"""Shared operations testing helpers."""

from typing import Any, Dict, Tuple, Type

from text_lint.__helpers__.translations import as_translation
from text_lint.operations.bases.operation_base import OperationBase

AliasOperationAttributes = Dict[str, Any]

REQUIRED_ATTRIBUTES = ["hint", "operation", "yaml_example"]


def assert_operation_attributes(
    operation_instance: "OperationBase",
    attributes: AliasOperationAttributes,
) -> None:

  for required_attribute in REQUIRED_ATTRIBUTES:
    assert required_attribute in attributes

  for attribute_name, attribute_value in attributes.items():
    attribute = getattr(operation_instance, attribute_name)
    if attribute_name == "hint":
      assert attribute == as_translation(attribute_value)
    else:
      assert attribute == attribute_value


def assert_operation_inheritance(
    operation_instance: "OperationBase",
    bases: Tuple[Type["OperationBase"], ...] = (),
) -> None:
  assert isinstance(
      operation_instance,
      OperationBase,
  )
  for base in bases:
    assert isinstance(
        operation_instance,
        base,
    )
