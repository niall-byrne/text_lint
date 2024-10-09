"""Test the LocalFolderExtensionsLoader class."""

import os
from typing import List, Tuple
from unittest import mock

import pytest
from text_lint.exceptions.external import ExternalLoaderFailedImport
from ..bases.loader_base import ExternalLoaderBase
from ..local import LocalFolderExtensionsLoader


class TestLocalFolderExtensionsLoader:
  """Test the LocalFolderExtensionsLoader class."""

  def test_initialize__attributes(
      self,
      mocked_paths: List[str],
      local_folder_extensions_loader_instance: LocalFolderExtensionsLoader,
  ) -> None:
    assert local_folder_extensions_loader_instance.local_paths == mocked_paths

  def test_initialize__inheritance(
      self,
      local_folder_extensions_loader_instance: LocalFolderExtensionsLoader,
  ) -> None:
    assert isinstance(
        local_folder_extensions_loader_instance,
        LocalFolderExtensionsLoader,
    )
    assert isinstance(
        local_folder_extensions_loader_instance,
        ExternalLoaderBase,
    )

  @pytest.mark.usefixtures(
      "scenario__local__valid_files__valid_specs__valid_modules"
  )
  def test_load_modules__valid_all__correct_modules(
      self,
      mocked_files: List[Tuple[bool, str]],
      mocked_paths: List[str],
      local_folder_extensions_loader_instance: LocalFolderExtensionsLoader,
  ) -> None:
    modules = local_folder_extensions_loader_instance.load_modules()

    module_index = 0
    for path_name in mocked_paths:
      for file in mocked_files:
        if file[0] and file[1].endswith(".py"):
          assert modules[module_index].from_spec.from_file == file[1]
          assert modules[module_index].from_spec.from_dir == path_name
          module_index += 1

    assert module_index == len(modules)

  @pytest.mark.usefixtures(
      "scenario__local__valid_files__valid_specs__valid_modules"
  )
  def test_load_modules__valid_all__calls_importlib(
      self,
      mocked_importlib: mock.Mock,
      local_folder_extensions_loader_instance: LocalFolderExtensionsLoader,
  ) -> None:
    modules = local_folder_extensions_loader_instance.load_modules()

    for module in modules:
      mocked_importlib.util.spec_from_file_location(
          module.from_spec.from_dir,
          module.from_spec.from_file,
      )
      mocked_importlib.util.module_from_spec(module.from_spec)
      module.from_spec.loader.exec_module.called_once_with(module)

  @pytest.mark.usefixtures(
      "scenario__local__invalid_files__valid_specs__valid_modules"
  )
  def test_load_modules__invalid_files__no_modules(
      self,
      local_folder_extensions_loader_instance: LocalFolderExtensionsLoader,
  ) -> None:
    modules = local_folder_extensions_loader_instance.load_modules()

    assert len(modules) == 0

  @pytest.mark.usefixtures(
      "scenario__local__valid_files__invalid_specs__valid_modules"
  )
  def test_load_modules__invalid_specs__exception(
      self,
      mocked_paths: List[str],
      mocked_files: List[Tuple[bool, str]],
      local_folder_extensions_loader_instance: LocalFolderExtensionsLoader,
  ) -> None:

    with pytest.raises(ExternalLoaderFailedImport) as exc:
      local_folder_extensions_loader_instance.load_modules()

    assert str(exc.value) == os.path.join(mocked_paths[0], mocked_files[1][1])

  @pytest.mark.usefixtures(
      "scenario__local__valid_files__valid_specs__invalid_modules"
  )
  def test_load_modules__invalid_modules__exception(
      self,
      local_folder_extensions_loader_instance: LocalFolderExtensionsLoader,
  ) -> None:

    with pytest.raises(ImportError):
      local_folder_extensions_loader_instance.load_modules()
