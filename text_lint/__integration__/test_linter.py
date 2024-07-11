"""Linter integration testing."""

from typing import TYPE_CHECKING, Callable, Optional, Type

import pytest
from text_lint.config import NEW_LINE
from text_lint.exceptions.assertions import AssertionViolation
from text_lint.exceptions.sequencers import UnconsumedData

if TYPE_CHECKING:
  from text_lint.linter import Linter


class TestLinter:
  """Linter integration testing."""

  data_valid = (NEW_LINE + "a" + NEW_LINE) * 10
  data_invalid = (NEW_LINE + "a" + NEW_LINE) * 8 + "a"
  data_short = (NEW_LINE + "a" + NEW_LINE) * 5

  def call_linter(
      self,
      linter: "Linter",
      exception: Optional[Type[Exception]],
  ) -> None:
    if exception:
      with pytest.raises(exception):
        linter.start()
    else:
      linter.start()

  @pytest.mark.parametrize(
      "data,exception",
      [
          [data_valid, None],
          [data_invalid, AssertionViolation],
          [data_short, UnconsumedData],
      ],
      ids=["valid", "invalid", "short"],
  )
  def test_simple_sequence__vary_file__raises_correct_exception(
      self,
      create_linter_instance: Callable[[str, str], "Linter"],
      yaml_simple_sequence: str,
      data: str,
      exception: Optional[Type[Exception]],
  ) -> None:
    linter = create_linter_instance(yaml_simple_sequence, data)

    self.call_linter(linter, exception)

  @pytest.mark.parametrize(
      "data,exception",
      [
          [data_valid, None],
          [data_invalid, AssertionViolation],
          [data_short, UnconsumedData],
      ],
      ids=["valid", "invalid", "short"],
  )
  def test_nested_sequence__vary_file__raises_correct_exception(
      self,
      create_linter_instance: Callable[[str, str], "Linter"],
      yaml_nested_sequence: str,
      data: str,
      exception: Optional[Type[Exception]],
  ) -> None:
    linter = create_linter_instance(yaml_nested_sequence, data)

    self.call_linter(linter, exception)

  @pytest.mark.parametrize(
      "data,exception",
      [
          [data_valid, None],
          [data_invalid, AssertionViolation],
          [data_short, None],
      ],
      ids=["valid", "invalid", "short"],
  )
  def test_infinite_sequence__vary_file__raises_correct_exception(
      self,
      create_linter_instance: Callable[[str, str], "Linter"],
      yaml_infinite_sequence: str,
      data: str,
      exception: Optional[Type[Exception]],
  ) -> None:
    linter = create_linter_instance(yaml_infinite_sequence, data)

    self.call_linter(linter, exception)

  @pytest.mark.parametrize(
      "data,exception",
      [
          [data_valid, None],
          [data_invalid, AssertionViolation],
          [data_short, None],
      ],
      ids=["valid", "invalid", "short"],
  )
  def test_nested_infinite_sequence__vary_file__raises_correct_exception(
      self,
      create_linter_instance: Callable[[str, str], "Linter"],
      yaml_nested_infinite_sequence: str,
      data: str,
      exception: Optional[Type[Exception]],
  ) -> None:
    linter = create_linter_instance(yaml_nested_infinite_sequence, data)

    self.call_linter(linter, exception)
