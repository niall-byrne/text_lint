"""Test AssertRegex class."""

from unittest import mock

import pytest
from text_lint.__helpers__.assertion import (
    assert_assertion_attributes,
    assert_is_assertion_violation,
)
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.results import assert_result_tree
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.assertions import AssertionViolation
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.assertions.bases.assertion_regex_base import (
    AssertionRegexBase,
)
from ..assert_regex import AssertRegex


class TestAssertRegex:
  """Test the AssertRegex class."""

  def test_initialize__defaults__attributes(self) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "this line must match the regex",
        "name": "example assert regex assertion",
        "operation": "assert_regex",
        "regex": "^([a-z-]+):\\s.+$",
        "save": None,
        "splits": {},
    }

    instance = AssertRegex(
        name="example assert regex assertion",
        regex="^([a-z-]+):\\s.+$",
    )

    assert_assertion_attributes(instance, attributes)

  def test_initialize__defined__attributes(
      self,
      assert_regex_instance: AssertRegex,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "this line must match the regex",
        "name": "example assert regex assertion",
        "operation": "assert_regex",
        "regex": "^([a-z-]+):\\s.+$",
        "save": "example",
        "splits": {
            1: " "
        }
    }

    assert_assertion_attributes(assert_regex_instance, attributes)

  def test_initialize__translations(
      self,
      assert_regex_instance: AssertRegex,
  ) -> None:
    assert_is_translated(assert_regex_instance.hint)

  def test_initialize__inheritance(
      self,
      assert_regex_instance: AssertRegex,
  ) -> None:
    assert_operation_inheritance(
        assert_regex_instance,
        bases=(
            AssertionBase,
            AssertionRegexBase,
            AssertRegex,
        ),
    )

  def test_apply__matches__stores_result(
      self,
      assert_regex_instance: AssertRegex,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.__next__.return_value = "matching: string"

    assert_regex_instance.apply(mocked_controller)

    assert len(mocked_controller.forest.add.mock_calls) == 1
    result_tree = mocked_controller.forest.add.mock_calls[0].args[0]
    assert_result_tree(
        result_tree,
        assert_regex_instance.save,
        ["matching".split(" ")],
    )

  def test_apply__does_not_match__raises_exception(
      self,
      assert_regex_instance: AssertRegex,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.index = 1
    mocked_textfile.__next__.return_value = "non matching string"

    with pytest.raises(AssertionViolation) as exc:
      assert_regex_instance.apply(mocked_controller)

    mocked_controller.forest.add.assert_not_called()
    assert_is_assertion_violation(
        exc=exc,
        assertion=assert_regex_instance,
        textfile=mocked_textfile,
        expected=assert_regex_instance.regex.pattern,
    )
