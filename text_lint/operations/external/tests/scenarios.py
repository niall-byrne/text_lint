"""Test fixtures for the external extension loader scenarios."""
# pylint: disable=redefined-outer-name

import os
from typing import List, Tuple
from unittest import mock

import pytest

__all__ = (
    "scenario__local__valid_files__valid_specs__valid_modules",
    "scenario__local__invalid_files__valid_specs__valid_modules",
    "scenario__local__valid_files__invalid_specs__valid_modules",
    "scenario__local__valid_files__valid_specs__invalid_modules",
)


@pytest.fixture
def scenario__local__valid_files__valid_specs__valid_modules(
    mocked_files: List[Tuple[bool, str]],
    mocked_importlib: mock.Mock,
    mocked_scandir: mock.Mock,
) -> None:
  mocked_scandir.side_effect = (
      lambda path: [
          mock.Mock(
              **{
                  "is_file.return_value": file_definition[0],
                  "path": os.path.join(path, file_definition[1]),
              }
          ) for file_definition in mocked_files
      ]
  )
  mocked_importlib.util.spec_from_file_location.side_effect = (
      lambda dirname, filename: mock.
      Mock(**{
          "from_file": os.path.basename(filename),
          "from_dir": dirname
      })
  )
  mocked_importlib.util.module_from_spec.side_effect = (
      lambda spec: mock.Mock(**{"from_spec": spec})
  )


@pytest.fixture
def scenario__local__invalid_files__valid_specs__valid_modules(
    # pylint: disable=unused-argument
    scenario__local__valid_files__valid_specs__valid_modules: None,
    mocked_files: List[Tuple[bool, str]],
    mocked_scandir: mock.Mock,
) -> None:
  mocked_scandir.side_effect = (
      lambda path: [
          mock.Mock(
              **{
                  "is_file.return_value": False,
                  "path": os.path.join(path, file_definition[1]),
              }
          ) for file_definition in mocked_files
      ]
  )


@pytest.fixture
def scenario__local__valid_files__invalid_specs__valid_modules(
    # pylint: disable=unused-argument
    scenario__local__valid_files__valid_specs__valid_modules: None,
    mocked_importlib: mock.Mock,
) -> None:
  mocked_importlib.util.spec_from_file_location.side_effect = None
  mocked_importlib.util.spec_from_file_location.return_value = None


@pytest.fixture
def scenario__local__valid_files__valid_specs__invalid_modules(
    # pylint: disable=unused-argument
    scenario__local__valid_files__valid_specs__valid_modules: None,
    mocked_importlib: mock.Mock,
) -> None:
  mocked_spec = mock.Mock(**{"loader.exec_module.side_effect": ImportError})
  mocked_importlib.util.spec_from_file_location.side_effect = None
  mocked_importlib.util.spec_from_file_location.return_value = mocked_spec
