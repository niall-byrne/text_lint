"""Test AssertSequenceEnds class."""

from unittest import mock

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.rules import assert_rule_attributes
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.operations.rules.bases.rule_base import RuleBase
from ..assert_sequence_ends import AssertSequenceEnds


class TestAssertSequenceEnds:
  """Test the AssertSequenceEnds class."""

  def test_initialize__defined__attributes(
      self,
      assert_sequence_ends_instance: AssertSequenceEnds,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "reserved",
        "matches": [],
        "name": "example assert sequence ends rule",
        "operation": "assert_sequence_ends",
        "save": None,
        "splits": {},
    }

    assert_rule_attributes(assert_sequence_ends_instance, attributes)

  def test_initialize__translations(
      self,
      assert_sequence_ends_instance: AssertSequenceEnds,
  ) -> None:
    assert_is_translated(assert_sequence_ends_instance.hint)

  def test_initialize__inheritance(
      self,
      assert_sequence_ends_instance: AssertSequenceEnds,
  ) -> None:
    assert_operation_inheritance(
        assert_sequence_ends_instance,
        bases=(
            RuleBase,
            AssertSequenceEnds,
        ),
    )

  def test_apply__calls_parser_methods(
      self,
      assert_sequence_ends_instance: AssertSequenceEnds,
      mocked_controller: mock.Mock,
  ) -> None:
    assert_sequence_ends_instance.apply(mocked_controller)

    mocked_controller.rules.stop_repeating.assert_called_once_with()
