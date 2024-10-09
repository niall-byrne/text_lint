"""Shared test fixtures for CLI argument types."""

from unittest import mock

import pytest
from .. import directory_type, file_type


@pytest.fixture
def mocked_os(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(directory_type, "os", instance)
  monkeypatch.setattr(file_type, "os", instance)
  return instance


@pytest.fixture
def mocked_path() -> str:
  return "mocked_file_name"
