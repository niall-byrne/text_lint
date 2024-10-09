"""Test the directory_type CLI argument type."""
from unittest import mock

import pytest
from .. import directory_type


class TestDirectoryType:
  """Test the directory_type CLI argument type."""

  def test_file_exists__is_dir__returns_absolute_path(
      self, mocked_path: str, mocked_os: mock.Mock
  ) -> None:
    mocked_os.path.exists.return_value = True
    mocked_os.path.isdir.return_value = True

    result = directory_type.directory_type(mocked_path)

    assert result == mocked_os.path.abspath.return_value
    mocked_os.path.abspath.assert_called_once_with(mocked_path)

  def test_file_exists__is_not_dir__raise_exception(
      self,
      mocked_path: str,
      mocked_os: mock.Mock,
  ) -> None:
    mocked_os.path.exists.return_value = True
    mocked_os.path.isdir.return_value = False

    with pytest.raises(NotADirectoryError) as exc:
      directory_type.directory_type(mocked_path)

    assert str(exc.value) == mocked_path

  def test_file_does_not_exist__raises_exception(
      self, mocked_path: str, mocked_os: mock.Mock
  ) -> None:
    mocked_os.path.exists.return_value = False

    with pytest.raises(FileNotFoundError) as exc:
      directory_type.directory_type(mocked_path)

    assert str(exc.value) == mocked_path
