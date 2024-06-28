"""Test AssertSequenceEnds class."""

from unittest import mock

from text_lint.__helpers__.assertion import assert_assertion_attributes
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from ..assert_sequence_ends import AssertSequenceEnds


class TestAssertSequenceEnds:
  """Test the AssertSequenceEnds class."""

  def test_initialize__defined__attributes(
      self,
      assert_sequence_ends_instance: AssertSequenceEnds,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "reserved",
        "name": "example assert sequence ends assertion",
        "operation": "assert_sequence_ends",
        "save": None,
        "splits": {},
    }

    assert_assertion_attributes(assert_sequence_ends_instance, attributes)

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
            AssertionBase,
            AssertSequenceEnds,
        ),
    )

  def test_apply__calls_parser_methods(
      self,
      assert_sequence_ends_instance: AssertSequenceEnds,
      mocked_controller: mock.Mock,
  ) -> None:
    assert_sequence_ends_instance.apply(mocked_controller)

    mocked_controller.assertions.stop_repeating.assert_called_once_with()
