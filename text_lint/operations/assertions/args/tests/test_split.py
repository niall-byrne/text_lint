"""Test the Split class."""
import pytest
from text_lint.__helpers__.operations import assert_parameter_schema
from text_lint.operations.mixins.parameter_validation import validators
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

    with pytest.raises(TypeError):
      Split(group=-1, separator="-")

  def test_initialize__parameters(self) -> None:
    instance = Split(group=1)

    assert_parameter_schema(
        instance=instance,
        parameter_definitions={
            "group":
                {
                    "type":
                        int,
                    "validators":
                        [validators.create_is_greater_than_or_equal(1),],
                },
            "separator": {
                "type": str,
                "optional": True
            },
        },
    )
