"""Test the file_type CLI argument type."""
from unittest import mock

import pytest
from .. import file_type


class TestFileType:
  """Test the file_type CLI argument type."""

  def test_file_exists__is_file__returns_absolute_path(
      self, mocked_path: str, mocked_os: mock.Mock
  ) -> None:
    mocked_os.path.exists.return_value = True
    mocked_os.path.isfile.return_value = True

    result = file_type.file_type(mocked_path)

    assert result == mocked_os.path.abspath.return_value
    mocked_os.path.abspath.assert_called_once_with(mocked_path)

  def test_file_exists__is_not_file__raise_exception(
      self,
      mocked_path: str,
      mocked_os: mock.Mock,
  ) -> None:
    mocked_os.path.exists.return_value = True
    mocked_os.path.isfile.return_value = False

    with pytest.raises(IsADirectoryError) as exc:
      file_type.file_type(mocked_path)

    assert str(exc.value) == mocked_path

  def test_file_does_not_exist__raises_exception(
      self, mocked_path: str, mocked_os: mock.Mock
  ) -> None:
    mocked_os.path.exists.return_value = False

    with pytest.raises(FileNotFoundError) as exc:
      file_type.file_type(mocked_path)

    assert str(exc.value) == mocked_path
