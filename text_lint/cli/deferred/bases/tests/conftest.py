"""Shared test fixtures for the CLI deferred loader base classes."""
# pylint: disable=redefined-outer-name

from typing import Type
from unittest import mock

import pytest
from .. import deferred_base


@pytest.fixture
def mocked_attribute() -> str:
  return "mocked_attribute"


@pytest.fixture
def mocked_importlib_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_module_path() -> str:
  return "mocked.module.path"


@pytest.fixture
def concrete_deferred_module_loader_base_class(
    mocked_attribute: str,
    mocked_module_path: str,
) -> Type[deferred_base.DeferredModuleLoaderBase[mock.Mock]]:

  class ConcreteModuleLoader(
      deferred_base.DeferredModuleLoaderBase[mock.Mock],
  ):

    module_attribute = mocked_attribute
    module_path = mocked_module_path

  return ConcreteModuleLoader


@pytest.fixture
def concrete_deferred_module_loader_base_instance(
    concrete_deferred_module_loader_base_class: (
        Type[deferred_base.DeferredModuleLoaderBase[mock.Mock]]
    ),
    mocked_importlib_module: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> deferred_base.DeferredModuleLoaderBase[mock.Mock]:
  monkeypatch.setattr(
      deferred_base,
      "importlib",
      mocked_importlib_module,
  )

  return concrete_deferred_module_loader_base_class()
