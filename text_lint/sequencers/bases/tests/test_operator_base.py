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

  def test_insert__infinite_count__inserts_assertions_correctly(
      self,
      concrete_operator_class: Type["OperatorBase[mock.Mock]"],
      mocked_operations: List["mock.Mock"],
  ) -> None:
    mocked_new_assertions = [mock.Mock(), mock.Mock(), mock.Mock()]
    instance = concrete_operator_class(mocked_operations)
    instance.index = 1

    instance.insert(mocked_new_assertions, -1)

    instance.index = 0

    assertions = [next(instance) for _ in range(0, 100)]
    assert assertions == mocked_operations[:1] + mocked_new_assertions * 33

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
