"""Test the SequencerBase class."""

from typing import List, Type
from unittest import mock

import pytest
from text_lint.config import LOOP_COUNT
from text_lint.sequencers.bases.operator_base import OperatorBase
from text_lint.sequencers.bases.sequencer_base import SequencerBase
from text_lint.sequencers.patterns.linear import LinearPattern
from text_lint.sequencers.patterns.loop import LinearLoopPattern


class TestOperatorBase:
  """Test the SequencerBase class."""

  def test_initialize__attributes(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)

    assert instance.index == 0
    assert isinstance(instance.pattern, LinearPattern)

  def test_initialize__inheritance(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)

    assert isinstance(instance, SequencerBase)
    assert isinstance(instance, OperatorBase)

  @pytest.mark.parametrize("count", [2, 4, 6])
  def test_len__vary_operation_count__returns_expected_value(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      count: int,
  ) -> None:
    instance = concrete_operator_class([mock.Mock()] * count)

    assert len(instance) == count

  def test_current__returns_current_element(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)

    for _ in instance:
      if instance.index < len(mocked_operations):
        assert instance.current == mocked_operations[instance.index]

  @pytest.mark.parametrize("count", [2, 4, 6])
  def test_insert__vary_bounded_count__inserts_assertions_correctly(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
      count: int,
  ) -> None:
    mocked_new_assertions = [mock.Mock()]
    instance = concrete_operator_class(mocked_operations)
    instance.index = 1

    instance.insert(mocked_new_assertions, count)

    instance.index = 0
    assertions = list(instance)
    assert assertions == (
        mocked_operations[:1] + mocked_new_assertions * count +
        mocked_operations[1:]
    )

  @pytest.mark.parametrize("entity_count", [2, 4, 6])
  def test_insert__vary_entity_count__bounded__calls_pattern_adjust_method(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
      monkeypatch: pytest.MonkeyPatch,
      entity_count: int,
  ) -> None:
    mocked_pattern = mock.Mock()
    instance = concrete_operator_class(mocked_operations)
    monkeypatch.setattr(
        instance,
        "pattern",
        mocked_pattern,
    )

    instance.insert([mock.Mock()] * entity_count, 1)

    mocked_pattern.adjust.assert_called_once_with(entity_count)

  def test_insert__infinite_count__inserts_assertions_correctly(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    mocked_new_assertions = [mock.Mock(), mock.Mock(), mock.Mock()]
    instance = concrete_operator_class(mocked_operations)
    instance.index = 1

    instance.insert(mocked_new_assertions, LOOP_COUNT)

    instance.index = 0

    assertions = [next(instance) for _ in range(0, 100)]
    assert assertions == mocked_operations[:1] + mocked_new_assertions * 33

  @pytest.mark.parametrize("entity_count", [2, 4, 6])
  def test_insert__vary_entity_count__infinite__assigns_loop_pattern(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
      entity_count: int,
  ) -> None:
    instance = concrete_operator_class(mocked_operations)
    expected_start = instance.index
    expected_end = instance.index + entity_count

    instance.insert([mock.Mock()] * entity_count, LOOP_COUNT)

    assert isinstance(instance.pattern, LinearLoopPattern)
    assert instance.pattern.start == expected_start
    assert instance.pattern.end == expected_end

  def test_iter__returns_iterator(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)

    iter_instance = iter(instance)

    assert iter_instance == instance

  def test_last__returns_previous_element(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)

    for _ in instance:
      if instance.index > -1:
        assert instance.last == mocked_operations[instance.index - 1]

  def test_next__available_operation__returns_next_operation(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)
    received: List["mock.Mock"] = []

    received += [next(instance) for _ in range(0, len(mocked_operations))]

    assert received == mocked_operations

  def test_next__no_operations__raises_stop_iteration(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)
    instance.index = 3

    with pytest.raises(StopIteration):
      next(instance)
