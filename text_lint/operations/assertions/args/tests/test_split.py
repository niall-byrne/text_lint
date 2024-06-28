"""Test the Split class."""
import pytest
from text_lint.exceptions.schema import SplitGroupInvalid
from ..split import Split


class TestSplit:
  """Test the Split class."""

  def test_intialize__default__attributes(self) -> None:
    instance = Split(group=1,)

    assert instance.group == 1
    assert instance.separator is None

  def test_intialize__defined__attributes(self) -> None:
    instance = Split(group=1, separator="-")

    assert instance.group == 1
    assert instance.separator == "-"

  def test_intialize__invalid__attributes(self) -> None:

    with pytest.raises(SplitGroupInvalid):
      Split(group=-1, separator="-")
