"""Test fixtures for the schema base classes."""
# pylint: disable=redefined-outer-name

from typing import Any, Dict, Type
from unittest import mock

import pytest
from text_lint.__fixtures__.mocks import AliasSpyOnMethod
from text_lint.schema import Schema
from .. import section_base


@pytest.fixture
def mocked_create_operation_instance_hook(
    concrete_schema_section_instance:
    "section_base.SchemaSectionBase[mock.Mock]",
    spy_on_method: "AliasSpyOnMethod"
) -> mock.Mock:
  return spy_on_method(
      concrete_schema_section_instance.hook_create_operation_instance
  )


@pytest.fixture
def mocked_load_operation_instances_hook(
    concrete_schema_section_instance:
    "section_base.SchemaSectionBase[mock.Mock]",
    spy_on_method: "AliasSpyOnMethod"
) -> mock.Mock:
  return spy_on_method(
      concrete_schema_section_instance.hook_load_operation_instances
  )


@pytest.fixture
def mocked_operation_classes() -> Dict[str, mock.Mock]:

  class OperationA(mock.Mock):
    operation = "A"
    hint = "hint_a"
    internal_use_only = False

  class OperationB(mock.Mock):
    operation = "B"
    hint = "hint_b"
    internal_use_only = False

  class OperationC(mock.Mock):
    operation = "C"
    hint = "hint_c"
    internal_use_only = False

  return {"A": OperationA(), "B": OperationB(), "C": OperationC()}


@pytest.fixture
def mocked_schema() -> mock.Mock:

  class MockedSchema(mock.Mock):
    path = "mocked_schema_file.yml"

    # pylint: disable=no-self-argument
    def create_exception(*args: Any, **kwargs: Any) -> Any:
      return getattr(Schema, "create_exception")(*args, **kwargs)

  return MockedSchema()


@pytest.fixture
def concrete_schema_section_class(
    mocked_operation_classes: Dict[str, Type[mock.Mock]],
) -> "Type[section_base.SchemaSectionBase[mock.Mock]]":

  class ConcreteSchemaSection(section_base.SchemaSectionBase[mock.Mock]):
    operation_classes = mocked_operation_classes
    schema_section_method = "mocked_section"
    entity_name = "mocked_entity"

  return ConcreteSchemaSection


@pytest.fixture
def concrete_schema_section_instance(
    concrete_schema_section_class:
    "Type[section_base.SchemaSectionBase[mock.Mock]]",
    mocked_schema: mock.Mock,
) -> "section_base.SchemaSectionBase[mock.Mock]":
  return concrete_schema_section_class(mocked_schema)
