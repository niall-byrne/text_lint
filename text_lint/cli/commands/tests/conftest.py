"""Shared test fixtures for the text_lint CLI commands."""
# pylint: disable=redefined-outer-name

from typing import List
from unittest import mock

import pytest
from .. import check_command, documentation_command, list_command


@pytest.fixture
def mocked_args_check() -> mock.Mock:
  instance = mock.Mock()
  instance.filenames = ["1.txt", "2.txt", "3.txt"]
  instance.quiet = True
  instance.schema = "/path/to/schema.yml"
  return instance


@pytest.fixture
def mocked_args_documentation() -> mock.Mock:
  instance = mock.Mock()
  instance.operations = ["operation1", "operation2", "operation3"]
  return instance


@pytest.fixture
def mocked_args_list() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_linter() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_linter_settings(
    mocked_linter_settings_instances: List[mock.Mock]
) -> mock.Mock:
  return mock.Mock(side_effect=mocked_linter_settings_instances)


@pytest.fixture
def mocked_linter_settings_instances() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_documentation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def check_command_instance(
    mocked_linter: mock.Mock,
    mocked_linter_settings: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> check_command.CheckCommand:
  monkeypatch.setattr(
      check_command,
      "Linter",
      mocked_linter,
  )
  monkeypatch.setattr(
      check_command,
      "LinterSettings",
      mocked_linter_settings,
  )
  return check_command.CheckCommand()


@pytest.fixture
def documentation_command_instance(
    mocked_documentation: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> documentation_command.DocumentationCommand:
  instance = documentation_command.DocumentationCommand()
  monkeypatch.setattr(
      instance,
      "documentation",
      mocked_documentation,
  )
  return instance


@pytest.fixture
def list_command_instance(
    mocked_documentation: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> list_command.ListCommand:
  instance = list_command.ListCommand()
  monkeypatch.setattr(
      instance,
      "documentation",
      mocked_documentation,
  )
  return instance
