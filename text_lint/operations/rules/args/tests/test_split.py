"""Test the Split class."""

from ..split import Split


class TestSplit:
  """Test the Split class."""

  def test_intialize__default__attributes(self) -> None:
    instance = Split(group=0,)

    assert instance.group == 0
    assert instance.separator is None

  def test_intialize__defined__attributes(self) -> None:
    instance = Split(group=1, separator="-")

    assert instance.group == 1
    assert instance.separator == "-"
