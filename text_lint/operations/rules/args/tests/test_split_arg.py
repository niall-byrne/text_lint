"""Test the SplitArgs class."""

from typing import Any, List, Optional

from ..split import Split, SplitArgs


class TestSplitArgs:
  """Test the SplitArgs class."""

  def assert_is_split(
      self,
      instance: Any,
      group: int,
      separator: Optional[str],
  ) -> None:
    assert isinstance(instance, Split)
    assert instance.group == group
    assert instance.separator == separator

  def test_intialize__attributes(
      self,
      split_instances: List[Split],
  ) -> None:
    instance = SplitArgs(splits=split_instances)

    assert instance.splits == split_instances

  def test_create__no_definition__does_not_create_splits(self) -> None:
    instance = SplitArgs.create([])

    assert len(instance.splits) == 0

  def test_create__single_definition__creates_single_split_instance(
      self
  ) -> None:
    instance = SplitArgs.create([{
        "group": 0,
    }])

    assert len(instance.splits) == 1
    self.assert_is_split(
        instance.splits[0],
        group=0,
        separator=None,
    )

  def test_create__multiple_definitions__creates_multiple_split_instances(
      self
  ) -> None:
    instance = SplitArgs.create(
        [{
            "group": 0,
        }, {
            "group": 1,
            "separator": "-"
        }]
    )

    assert len(instance.splits) == 2
    self.assert_is_split(
        instance.splits[0],
        group=0,
        separator=None,
    )
    self.assert_is_split(
        instance.splits[1],
        group=1,
        separator="-",
    )

  def test_as_dict__no_splits__correct_representation(self) -> None:
    instance = SplitArgs.create([])

    assert instance.as_dict() == {}

  def test_as_dict__single_split__correct_representation(self) -> None:
    instance = SplitArgs.create([{
        "group": 0,
    }])

    assert instance.as_dict() == {
        0: None,
    }

  def test_as_dict__multiple_splits__correct_representation(self) -> None:
    instance = SplitArgs.create(
        [{
            "group": 0,
        }, {
            "group": 1,
            "separator": "-"
        }]
    )

    assert instance.as_dict() == {
        0: None,
        1: "-",
    }
