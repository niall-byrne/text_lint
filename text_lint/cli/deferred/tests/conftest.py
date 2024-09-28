"""Shared test fixtures for the CLI deferred module loaders."""
# pylint: disable=redefined-outer-name

import pytest
from .. import (
    deferred_linter,
    deferred_linter_settings,
    deferred_operation_documentation,
)


@pytest.fixture
def deferred_linter_instance() -> deferred_linter.DeferredLinter:
  return deferred_linter.DeferredLinter()


@pytest.fixture
def deferred_linter_settings_instance(
) -> deferred_linter_settings.DeferredLinterSettings:
  return deferred_linter_settings.DeferredLinterSettings()


@pytest.fixture
def deferred_operation_documentation_instance(
) -> deferred_operation_documentation.DeferredOperationDocumentation:
  return deferred_operation_documentation.DeferredOperationDocumentation()
