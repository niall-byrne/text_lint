"""Test AssertBlank class."""

from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.rules import (
    assert_is_rule_violation,
    assert_rule_attributes,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.rules import RuleViolation
from text_lint.operations.rules.bases.rule_base import RuleBase
from text_lint.utilities.whitespace import new_line
from ..assert_blank import AssertBlank


class TestAssertBlank:
  """Test the AssertBlank class."""

  def test_initialize__defined__attributes(
      self,
      assert_blank_instance: AssertBlank,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "sections must be separated by blank lines",
        "matches": [],
        "name": "example assert blank rule",
        "operation": "assert_blank",
        "save": None,
        "splits": {},
    }

    assert_rule_attributes(assert_blank_instance, attributes)

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
        bases=(RuleBase, AssertBlank),
    )

  def test_apply__matches__does_not_store_result(
      self,
      assert_blank_instance: AssertBlank,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.__next__.return_value = new_line()

    assert_blank_instance.apply(mocked_controller)

    assert assert_blank_instance.matches == []

  def test_apply__does_not_match__raises_exception(
      self,
      assert_blank_instance: AssertBlank,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.index = 1
    mocked_textfile.__next__.return_value = "non matching string\n"

    with pytest.raises(RuleViolation) as exc:
      assert_blank_instance.apply(mocked_controller)

    assert assert_blank_instance.matches == []
    assert_is_rule_violation(
        exc=exc,
        rule=assert_blank_instance,
        textfile=mocked_textfile,
        expected=new_line(),
    )
