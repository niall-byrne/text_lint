"""Test the Split class."""
import pytest
from text_lint.exceptions.schema import SplitGroupInvalid
from ..split import Split


class TestSplit:
  """Test the Split class."""

  def test_initialize__default__attributes(self) -> None:
    instance = Split(group=1)

    assert instance.group == 1
    assert instance.separator is None

  def test_initialize__defined__attributes(self) -> None:
    instance = Split(group=1, separator="-")

    assert instance.group == 1
    assert instance.separator == "-"

  def test_initialize__invalid_split_group__raises_exception(self) -> None:

    with pytest.raises(SplitGroupInvalid):
      Split(group=-1, separator="-")
