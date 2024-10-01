"""Shared operations testing helpers."""

from typing import Any, Dict, Tuple, Type

from text_lint.__helpers__.translations import as_translation
from text_lint.operations.bases.operation_base import OperationBase

AliasOperationAttributes = Dict[str, Any]


def assert_operation_attributes(
    operation_instance: "OperationBase[Any]",
    attributes: AliasOperationAttributes,
) -> None:

  for attribute_name, attribute_value in attributes.items():
    attribute = getattr(operation_instance, attribute_name)
    if attribute_name == "hint":
      assert attribute == as_translation(attribute_value)
    else:
      assert attribute == attribute_value


def assert_operation_inheritance(
    operation_instance: "OperationBase[Any]",
    bases: Tuple[Type["OperationBase[Any]"], ...] = (),
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
