"""Test the LinearLoopPattern class."""

from unittest import mock

import pytest
from text_lint.sequencers.patterns.bases.pattern_base import (
    SequencerPatternBase,
)
from ..loop import LinearLoopPattern


class TestLinearLoopPattern:
  """Test the LinearLoopPattern class."""

  def test_initialize__attributes(
      self,
      mocked_end_point: int,
      mocked_start_point: int,
      loop_pattern_instance: LinearLoopPattern,
  ) -> None:
    assert loop_pattern_instance.end == mocked_end_point
    assert loop_pattern_instance.start == mocked_start_point

  def test_initialize__inheritance(
      self,
      loop_pattern_instance: LinearLoopPattern,
  ) -> None:
    assert isinstance(loop_pattern_instance, SequencerPatternBase)
    assert isinstance(loop_pattern_instance, LinearLoopPattern)

  @pytest.mark.parametrize("offset", [2, 4, 6])
  def test_adjust__changes_loop_end(
      self,
      mocked_end_point: int,
      loop_pattern_instance: LinearLoopPattern,
      offset: int,
  ) -> None:
    loop_pattern_instance.adjust(offset)

    assert loop_pattern_instance.end == mocked_end_point + offset

  @pytest.mark.parametrize("index", [2, 4, 6])
  def test_increment__vary_valid_index__inside_loop__increments_index_by_1(
      self,
      mocked_sequencer: mock.MagicMock,
      loop_pattern_instance: LinearLoopPattern,
      index: int,
  ) -> None:
    mocked_sequencer.__len__.return_value = loop_pattern_instance.end
    mocked_sequencer.index = index

    loop_pattern_instance.increment(mocked_sequencer)

    assert mocked_sequencer.index == index + 1

  @pytest.mark.parametrize("index_offset", [0, 1, 2])
  def test_increment__index_at_or_past_end_of_loop__raises_exception(
      self,
      mocked_sequencer: mock.MagicMock,
      loop_pattern_instance: LinearLoopPattern,
      index_offset: int,
  ) -> None:
    mocked_sequencer.__len__.return_value = loop_pattern_instance.end
    mocked_sequencer.index = loop_pattern_instance.end + index_offset

    loop_pattern_instance.increment(mocked_sequencer)

    assert mocked_sequencer.index == loop_pattern_instance.start
