"""Shared operations testing helpers."""

from typing import Any, Dict, Tuple, Type

import pytest
from text_lint.__helpers__.translations import (
    as_translation,
    assert_all_translated,
)
from text_lint.exceptions.operations import InvalidParameterValidation
from text_lint.operations.bases.operation_base import OperationBase
from text_lint.utilities.translations import f as translation_f

AliasOperationAttributes = Dict[str, Any]

REQUIRED_ATTRIBUTES = [
    "internal_use_only",
    "hint",
    "operation",
    "yaml_example",
]


def assert_is_invalid_parameter_validation(
    exc: pytest.ExceptionInfo[InvalidParameterValidation],
    description_t: Tuple[str, ...],
    detail_t: Tuple[str, ...],
    operation_class: "Any",
) -> None:
  expected_translation = []

  def f(*args: Any, nl: int = 0, **kwargs: Any) -> str:
    expected_translation.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)

  message = f(
      *description_t,
      nl=1,
  )
  message += f(
      InvalidParameterValidation.msg_fmt_operation_class,
      operation_class.__name__,
      nl=1,
  )
  message += f(
      InvalidParameterValidation.msg_fmt_detail,
      detail_t[0].format(*detail_t[1:]),
      nl=1,
  )

  assert exc.value.__class__ == InvalidParameterValidation
  assert exc.value.args[0] == message
  assert_all_translated(expected_translation)


def assert_operation_attributes(
    operation_instance: "OperationBase[Any]",
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
