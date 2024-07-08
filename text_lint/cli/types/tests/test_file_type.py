"""Test the file_type CLI argument type."""
from unittest import mock

import pytest
from .. import file_type


class TestFileType:
  """Test the file_type CLI argument type."""

  def test_file_exists__returns_absolute_path(
      self,
      mocked_file_name: str,
  ) -> None:
    with mock.patch(file_type.__name__ + ".os") as mocked_os:
      mocked_os.path.exists.return_value = True

      result = file_type.file_type(mocked_file_name)

    assert result == mocked_os.path.abspath.return_value
    mocked_os.path.abspath.assert_called_once_with(mocked_file_name)

  def test_file_does_not_exist__raises_exception(
      self,
      mocked_file_name: str,
  ) -> None:
    with mock.patch(file_type.__name__ + ".os") as mocked_os:
      mocked_os.path.exists.return_value = False

      with pytest.raises(FileNotFoundError) as exc:
        file_type.file_type(mocked_file_name)

    assert str(exc.value) == mocked_file_name
