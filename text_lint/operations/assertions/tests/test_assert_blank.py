"""Test AssertBlank class."""

from unittest import mock

from text_lint.__helpers__.assertion import assert_assertion_attributes
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from ..assert_blank import AssertBlank


class TestAssertBlank:
  """Test the AssertBlank class."""

  def test_initialize__defined__attributes(
      self,
      assert_blank_instance: AssertBlank,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "the line contains no text",
        "name": "example assert blank assertion",
        "operation": "assert_blank",
        "save": None,
        "splits": {},
    }

    assert_assertion_attributes(assert_blank_instance, attributes)

  def test_initialize__translations(
      self,
      assert_blank_instance: AssertBlank,
  ) -> None:
    assert_is_translated(assert_blank_instance.hint)

  def test_initialize__inheritance(
      self,
      assert_blank_instance: AssertBlank,
  ) -> None:
    assert_operation_inheritance(
        assert_blank_instance,
        bases=(AssertionBase, AssertBlank),
    )

  def test_apply__matches__does_not_save_result(
      self,
      assert_blank_instance: AssertBlank,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.next.return_value = ""

    assert_blank_instance.apply(mocked_state)

    mocked_state.save.assert_not_called()

  def test_apply__does_not_match__calls_fail(
      self,
      assert_blank_instance: AssertBlank,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.next.return_value = "non matching string"

    assert_blank_instance.apply(mocked_state)

    mocked_state.fail.assert_called_once_with("")
