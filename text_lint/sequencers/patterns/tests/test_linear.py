"""Test the LinearPattern class."""

from unittest import mock

import pytest
from text_lint.sequencers.patterns.bases.pattern_base import (
    SequencerPatternBase,
)
from ..linear import LinearPattern


class TestLinearPattern:
  """Test the LinearPattern class."""

  def test_initialize__inheritance(
      self,
      linear_pattern_instance: LinearPattern,
  ) -> None:
    assert isinstance(linear_pattern_instance, SequencerPatternBase)
    assert isinstance(linear_pattern_instance, LinearPattern)

  @pytest.mark.parametrize("offset", [2, 4, 6])
  def test_adjust__is_a_noop(
      self,
      linear_pattern_instance: LinearPattern,
      offset: int,
  ) -> None:
    linear_pattern_instance.adjust(offset)

  @pytest.mark.parametrize("index", [2, 4, 6])
  def test_increment__vary_index__valid_index__increments_index_by_1(
      self,
      mocked_sequencer: mock.MagicMock,
      linear_pattern_instance: LinearPattern,
      index: int,
  ) -> None:
    mocked_sequencer.__len__.return_value = index + 1
    mocked_sequencer.index = index

    linear_pattern_instance.increment(mocked_sequencer)

    assert mocked_sequencer.index == index + 1

  @pytest.mark.parametrize("index", [2, 4, 6])
  def test_increment__vary_index__invalid_index__raises_exception(
      self,
      mocked_sequencer: mock.MagicMock,
      linear_pattern_instance: LinearPattern,
      index: int,
  ) -> None:
    mocked_sequencer.__len__.return_value = index
    mocked_sequencer.index = index

    with pytest.raises(StopIteration):
      linear_pattern_instance.increment(mocked_sequencer)
