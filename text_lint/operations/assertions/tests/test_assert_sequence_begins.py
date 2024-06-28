"""Test AssertSequenceBegins class."""

from typing import List, Optional
from unittest import mock

import pytest
from text_lint.__helpers__.assertion import assert_assertion_attributes
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOP_COUNT
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from ..assert_sequence_begins import AssertSequenceBegins


class TestAssertSequenceBegins:
  """Test the AssertSequenceBegins class."""

  def test_initialize__defined__attributes(
      self,
      assert_sequence_begins_instance: AssertSequenceBegins,
      mocked_nested_assertions: List[mock.Mock],
  ) -> None:
    attributes: AliasOperationAttributes = {
        "count": 2,
        "hint": "identify a repeating sequence of assertions",
        "name": "example assert sequence begins assertion",
        "operation": "assert_sequence_begins",
        "assertions": mocked_nested_assertions,
        "save": None,
        "splits": {},
    }

    assert_assertion_attributes(assert_sequence_begins_instance, attributes)

  def test_initialize__translations(
      self,
      assert_sequence_begins_instance: AssertSequenceBegins,
  ) -> None:
    assert_is_translated(assert_sequence_begins_instance.hint)

  def test_initialize__inheritance(
      self,
      assert_sequence_begins_instance: AssertSequenceBegins,
  ) -> None:
    assert_operation_inheritance(
        assert_sequence_begins_instance,
        bases=(
            AssertionBase,
            AssertSequenceBegins,
        ),
    )

  @pytest.mark.parametrize("count", [LOOP_COUNT, 2, 4])
  def test_apply__infinite_or_bound_count__calls_parser_methods(
      self,
      assert_sequence_begins_instance: AssertSequenceBegins,
      mocked_controller: mock.Mock,
      count: Optional[int],
  ) -> None:
    setattr(assert_sequence_begins_instance, "count", count)

    assert_sequence_begins_instance.apply(mocked_controller)

    mocked_controller.assertions.start_repeating.assert_called_with(
        assert_sequence_begins_instance.count
    )
    mocked_controller.assertions.insert.assert_called_with(
        assert_sequence_begins_instance.assertions
    )

  @pytest.mark.parametrize("count", [0, -10])
  def test_apply__zero_count__does_not_call_parser_methods(
      self,
      assert_sequence_begins_instance: AssertSequenceBegins,
      mocked_controller: mock.Mock,
      count: Optional[int],
  ) -> None:
    setattr(assert_sequence_begins_instance, "count", count)

    assert_sequence_begins_instance.apply(mocked_controller)

    mocked_controller.assertions.assert_not_called()
