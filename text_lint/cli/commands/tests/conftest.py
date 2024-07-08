"""Shared test fixtures for the text_lint CLI commands."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from .. import check_command, documentation_command, list_command


@pytest.fixture
def mocked_controller() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_documentation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def check_command_instance(
    mocked_controller: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> check_command.CheckCommand:
  monkeypatch.setattr(
      check_command,
      "Controller",
      mocked_controller,
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
