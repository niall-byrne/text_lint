"""Test fixtures for the external extensions loaders."""
# pylint: disable=redefined-outer-name

from typing import List, Tuple
from unittest import mock

import pytest
from .. import local, third_party
# pylint: disable=wildcard-import,unused-wildcard-import
from .scenarios import *


@pytest.fixture
def mocked_files() -> List[Tuple[bool, str]]:
  return [
      (True, "non_python_file.txt"),
      (True, "python_module_a.py"),
      (True, "python_module_b.py"),
      (True, "python_module_c.py"),
      (False, "directory_a"),
      (False, "directory_b"),
  ]


@pytest.fixture
def mocked_importlib() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_module_names() -> List[str]:
  return [
      "library_a",
      "library_b.module",
      "library_c.module.module",
  ]


@pytest.fixture
def mocked_paths() -> List[str]:
  return [
      "folder1",
      "folder2",
      "folder3",
  ]


@pytest.fixture
def mocked_scandir() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def local_folder_extensions_loader_instance(
    mocked_importlib: mock.Mock,
    mocked_paths: List[str],
    mocked_scandir: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> local.LocalFolderExtensionsLoader:
  monkeypatch.setattr(
      local,
      "importlib",
      mocked_importlib,
  )
  monkeypatch.setattr(
      local.os,
      "scandir",
      mocked_scandir,
  )

  return local.LocalFolderExtensionsLoader(paths=mocked_paths)


@pytest.fixture
def third_party_extensions_loader_instance(
    mocked_importlib: mock.Mock,
    mocked_module_names: List[str],
    monkeypatch: pytest.MonkeyPatch,
) -> third_party.ThirdPartyExtensionsLoader:
  monkeypatch.setattr(
      third_party,
      "importlib",
      mocked_importlib,
  )
  return third_party.ThirdPartyExtensionsLoader(modules=mocked_module_names)
