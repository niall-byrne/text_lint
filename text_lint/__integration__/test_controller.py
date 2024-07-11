"""Controller integration testing."""

from typing import TYPE_CHECKING, Callable, Optional, Type

import pytest
from text_lint.config import NEW_LINE
from text_lint.exceptions.rules import RuleViolation
from text_lint.exceptions.sequencers import UnconsumedData

if TYPE_CHECKING:
  from text_lint.controller import Controller


class TestController:
  """Controller integration testing."""

  data_valid = (NEW_LINE + "a" + NEW_LINE) * 10
  data_invalid = (NEW_LINE + "a" + NEW_LINE) * 8 + "a"
  data_short = (NEW_LINE + "a" + NEW_LINE) * 5

  def call_controller(
      self,
      controller: "Controller",
      exception: Optional[Type[Exception]],
  ) -> None:
    if exception:
      with pytest.raises(exception):
        controller.start()
    else:
      controller.start()

  @pytest.mark.parametrize(
      "data,exception",
      [
          [data_valid, None],
          [data_invalid, RuleViolation],
          [data_short, UnconsumedData],
      ],
      ids=["valid", "invalid", "short"],
  )
  def test_simple_sequence__vary_file__raises_correct_exception(
      self,
      create_controller_instance: Callable[[str, str], "Controller"],
      yaml_simple_sequence: str,
      data: str,
      exception: Optional[Type[Exception]],
  ) -> None:
    controller = create_controller_instance(yaml_simple_sequence, data)

    self.call_controller(controller, exception)

  @pytest.mark.parametrize(
      "data,exception",
      [
          [data_valid, None],
          [data_invalid, RuleViolation],
          [data_short, UnconsumedData],
      ],
      ids=["valid", "invalid", "short"],
  )
  def test_nested_sequence__vary_file__raises_correct_exception(
      self,
      create_controller_instance: Callable[[str, str], "Controller"],
      yaml_nested_sequence: str,
      data: str,
      exception: Optional[Type[Exception]],
  ) -> None:
    controller = create_controller_instance(yaml_nested_sequence, data)

    self.call_controller(controller, exception)

  @pytest.mark.parametrize(
      "data,exception",
      [
          [data_valid, None],
          [data_invalid, RuleViolation],
          [data_short, None],
      ],
      ids=["valid", "invalid", "short"],
  )
  def test_infinite_sequence__vary_file__raises_correct_exception(
      self,
      create_controller_instance: Callable[[str, str], "Controller"],
      yaml_infinite_sequence: str,
      data: str,
      exception: Optional[Type[Exception]],
  ) -> None:
    controller = create_controller_instance(yaml_infinite_sequence, data)

    self.call_controller(controller, exception)

  @pytest.mark.parametrize(
      "data,exception",
      [
          [data_valid, None],
          [data_invalid, RuleViolation],
          [data_short, None],
      ],
      ids=["valid", "invalid", "short"],
  )
  def test_nested_infinite_sequence__vary_file__raises_correct_exception(
      self,
      create_controller_instance: Callable[[str, str], "Controller"],
      yaml_nested_infinite_sequence: str,
      data: str,
      exception: Optional[Type[Exception]],
  ) -> None:
    controller = create_controller_instance(yaml_nested_infinite_sequence, data)

    self.call_controller(controller, exception)
