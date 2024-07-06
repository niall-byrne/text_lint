"""Test fixtures for the text file linter."""
# pylint: disable=redefined-outer-name

from io import StringIO
from typing import TYPE_CHECKING, List, Type
from unittest import mock

import pytest
from text_lint import schema

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.schema import AliasYamlOperation


@pytest.fixture
def mocked_file_handle() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_open() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_operation_definitions() -> List["AliasYamlOperation"]:
  return [{"definition": 1}, {"definition": 2}]


@pytest.fixture
def mocked_operation_instances() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_schema() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_schema_file() -> str:
  return "mock_schema.yml"


@pytest.fixture
def mocked_schema_assertions_section() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_schema_validators_section() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def schema_class(
    mocked_file_handle: StringIO,
    mocked_open: mock.MagicMock,
    mocked_schema_assertions_section: mock.Mock,
    mocked_schema_validators_section: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[schema.Schema]:
  monkeypatch.setattr(
      schema,
      "SchemaAssertions",
      mocked_schema_assertions_section,
  )
  monkeypatch.setattr(
      schema,
      "SchemaValidators",
      mocked_schema_validators_section,
  )
  monkeypatch.setattr(
      "builtins.open",
      mocked_open,
  )
  mocked_open.return_value = mocked_file_handle
  return schema.Schema
