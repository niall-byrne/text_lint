"""Test the RecursionDetection class."""
from unittest import mock

import pytest
from text_lint.__helpers__.linter import (
    assert_is_linter_recursion_limit_exceeded,
)
from text_lint.config import LOOP_RECURSION_LIMIT
from text_lint.exceptions.linter import LinterRecursionLimitExceeded
from ..recursion import RecursionDetection


class TestRecursionDetection:
  """Test the RecursionDetection class."""

  def test_initialize__attributes(
      self,
      recursion_detection_instance: RecursionDetection,
      mocked_linter: mock.Mock,
  ) -> None:
    # pylint: disable=protected-access
    assert recursion_detection_instance._linter == mocked_linter
    assert recursion_detection_instance.index == -1
    assert recursion_detection_instance.count == 0

  def test_detect__index_does_not_match__count_set_to_zero(
      self, recursion_detection_instance: RecursionDetection,
      mocked_linter: mock.Mock
  ) -> None:
    mocked_linter.textfile.index = 100
    recursion_detection_instance.index = 91
    recursion_detection_instance.count = 10

    recursion_detection_instance.detect()

    assert recursion_detection_instance.count == 0

  def test_detect__index_matches__count_is_incremented(
      self, recursion_detection_instance: RecursionDetection,
      mocked_linter: mock.Mock
  ) -> None:
    mocked_linter.textfile.index = 100
    recursion_detection_instance.index = 100
    recursion_detection_instance.count = 10

    recursion_detection_instance.detect()

    assert recursion_detection_instance.count == 11

  def test_detect__index_matches__repeats_under_limit__no_exception(
      self, recursion_detection_instance: RecursionDetection,
      mocked_linter: mock.Mock
  ) -> None:
    mocked_linter.textfile.index = 100
    recursion_detection_instance.index = 100
    recursion_detection_instance.count = LOOP_RECURSION_LIMIT - 10

    for _ in range(10):
      recursion_detection_instance.detect()

  def test_detect__index_matches__repeats_until_limit__raises_exception(
      self, recursion_detection_instance: RecursionDetection,
      mocked_linter: mock.Mock
  ) -> None:
    mocked_linter.textfile.index = 100
    recursion_detection_instance.index = 100
    recursion_detection_instance.count = LOOP_RECURSION_LIMIT - 1

    with pytest.raises(LinterRecursionLimitExceeded) as exc:
      for _ in range(10):
        recursion_detection_instance.detect()

    assert_is_linter_recursion_limit_exceeded(
        exc=exc,
        linter=mocked_linter,
    )
