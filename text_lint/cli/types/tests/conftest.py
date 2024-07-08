"""Shared test fixtures for CLI argument types."""

import pytest


@pytest.fixture
def mocked_file_name() -> str:
  return "mocked_file_name"
