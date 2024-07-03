"""Test AssertSequenceBegins class."""

from typing import List, Optional
from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.rules import assert_rule_attributes
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.operations.rules.bases.rule_base import RuleBase
from ..assert_sequence_begins import YAML_EXAMPLE, AssertSequenceBegins


class TestAssertSequenceBegins:
  """Test the AssertSequenceBegins class."""

  def test_initialize__defined__attributes(
      self,
      assert_sequence_begins_instance: AssertSequenceBegins,
      mocked_nested_rules: List[mock.Mock],
  ) -> None:
    attributes: AliasOperationAttributes = {
        "count": 2,
        "hint": "identify a repeating sequence of parser rules",
        "matches": [],
        "name": "example assert sequence begins rule",
        "operation": "assert_sequence_begins",
        "rules": mocked_nested_rules,
        "save": None,
        "splits": {},
        "yaml_example": YAML_EXAMPLE,
    }

    assert_rule_attributes(assert_sequence_begins_instance, attributes)

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
            RuleBase,
            AssertSequenceBegins,
        ),
    )

  @pytest.mark.parametrize("count", [-1, 2, 4])
  def test_apply__infinite_or_bound_count__calls_parser_methods(
      self,
      assert_sequence_begins_instance: AssertSequenceBegins,
      mocked_controller: mock.Mock,
      count: Optional[int],
  ) -> None:
    setattr(assert_sequence_begins_instance, "count", count)

    assert_sequence_begins_instance.apply(mocked_controller)

    mocked_controller.rules.start_repeating.assert_called_with(
        assert_sequence_begins_instance.count
    )
    mocked_controller.rules.insert.assert_called_with(
        assert_sequence_begins_instance.rules
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

    mocked_controller.rules.assert_not_called()
