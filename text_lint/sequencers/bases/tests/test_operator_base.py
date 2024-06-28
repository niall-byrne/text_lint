"""Test the SequencerBase class."""

from typing import TYPE_CHECKING, List, Type
from unittest import mock

import pytest
from text_lint.sequencers.bases.operator_base import OperatorBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.bases.operation_base import OperationBase


class TestOperatorBase:
  """Test the SequencerBase class."""

  def test_initialize__attributes(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)

    assert instance.index == 0

  def test_insert__inserts_rules_in_correct_order(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    mocked_new_rules = [mock.Mock()]
    instance = concrete_operator_class(mocked_operations)
    instance.index = 1

    instance.insert(mocked_new_rules)

    instance.index = 0
    rules = list(instance)
    assert rules == (
        mocked_operations[:1] + mocked_new_rules + mocked_operations[1:]
    )

  def test_iter__returns_iterator(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)

    iter_instance = iter(instance)

    assert iter_instance == instance

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

  def test_start_repeating__bounded__creates_bounded_looping_pattern(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)

    instance.start_repeating(count=4)
    rules_list = list(instance)

    assert len(rules_list) == 3 * 4
    assert rules_list == mocked_operations * 4

  def test_start_repeating__infinite__creates_infinite_looping_pattern(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)

    instance.start_repeating(count=-1)
    rules_list = [next(instance) for _ in range(0, 6)]

    assert len(rules_list) == 6
    assert rules_list == mocked_operations * 2

  def test_stop_repeating__infinite__no_effect(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    instance = concrete_operator_class(mocked_operations)

    instance.start_repeating(count=-1)
    _ = [next(instance) for _ in range(0, 4)]
    instance.stop_repeating()
    _ = [next(instance) for _ in range(0, 4)]
