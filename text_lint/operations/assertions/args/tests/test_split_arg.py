"""Test the SplitArgs class."""

from typing import Any, List, Optional, cast

import pytest
from text_lint.__helpers__.translations import assert_is_translated
from ..split import AliasYamlSplit, Split, SplitArgs


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

  def test_intialize__translations(self) -> None:
    assert_is_translated(SplitArgs.msg_fmt_invalid_splits)

  def test_create__no_definition__does_not_create_splits(self) -> None:
    instance = SplitArgs.create([])

    assert len(instance.splits) == 0

  def test_create__single_definition__creates_single_split_instance(
      self
  ) -> None:
    instance = SplitArgs.create([{
        "group": 1,
    }])

    assert len(instance.splits) == 1
    self.assert_is_split(
        instance.splits[0],
        group=1,
        separator=None,
    )

  def test_create__multiple_definitions__creates_multiple_split_instances(
      self
  ) -> None:
    instance = SplitArgs.create(
        [{
            "group": 1,
        }, {
            "group": 2,
            "separator": "-"
        }]
    )

    assert len(instance.splits) == 2
    self.assert_is_split(
        instance.splits[0],
        group=1,
        separator=None,
    )
    self.assert_is_split(
        instance.splits[1],
        group=2,
        separator="-",
    )

  def test_create__invalid_yaml__raises_exception(self) -> None:
    with pytest.raises(TypeError) as exc:
      SplitArgs.create(cast(AliasYamlSplit, "invalid yaml"))

    assert str(exc.value) == \
        SplitArgs.msg_fmt_invalid_splits.format("invalid yaml")

  def test_as_dict__no_splits__correct_representation(self) -> None:
    instance = SplitArgs.create([])

    assert instance.as_dict() == {}

  def test_as_dict__single_split__correct_representation(self) -> None:
    instance = SplitArgs.create([{
        "group": 1,
    }])

    assert instance.as_dict() == {
        1: None,
    }

  def test_as_dict__multiple_splits__correct_representation(self) -> None:
    instance = SplitArgs.create(
        [{
            "group": 1,
        }, {
            "group": 2,
            "separator": "-"
        }]
    )

    assert instance.as_dict() == {
        1: None,
        2: "-",
    }
