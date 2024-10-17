"""Test the Split class."""
from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    assert_parameter_schema,
    spy_on_validate_parameters,
)
from text_lint.operations.mixins.parameter_validation import (
    validator_factories,
)
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

  @spy_on_validate_parameters(Split)
  def test_initialize__parameter_validation(
      self,
      validate_parameters_spy: mock.Mock,
  ) -> None:
    instance = Split(group=1)

    assert_parameter_schema(
        instance=instance,
        parameter_definitions={
            "group":
                {
                    "type":
                        int,
                    "validators":
                        [
                            validator_factories.
                            create_is_greater_than_or_equal(1)
                        ],
                },
            "separator": {
                "type": str,
                "optional": True
            },
        },
    )
    validate_parameters_spy.assert_called_once_with(instance)
