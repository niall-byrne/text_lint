"""Test AssertEqual class."""

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
from ..assert_equal import AssertEqual
from .conftest import CaseSensitivityScenario


class TestAssertEqual:
  """Test the AssertEqual class."""

  def test_initialize__defaults__attributes(self) -> None:
    attributes: AliasOperationAttributes = {
        "case_sensitive": True,
        "expected": "#!/usr/bin/make -f",
        "hint": "this line must match the expected value",
        "name": "example assert equal assertion",
        "operation": "assert_equal",
        "regex": "(.*)",
        "save": None,
        "splits": {},
    }

    instance = AssertEqual(
        name="example assert equal assertion",
        expected="#!/usr/bin/make -f",
    )

    assert_assertion_attributes(instance, attributes)

  def test_initialize__defined__attributes(
      self,
      assert_equal_instance: AssertEqual,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "case_sensitive": False,
        "expected": "#!/usr/bin/make -f",
        "hint": "this line must match the expected value",
        "name": "example assert equal assertion",
        "operation": "assert_equal",
        "regex": "(.*)",
        "save": "example",
        "splits": {
            1: "/"
        },
    }

    assert_assertion_attributes(assert_equal_instance, attributes)

  def test_initialize__translations(
      self,
      assert_equal_instance: AssertEqual,
  ) -> None:
    assert_is_translated(assert_equal_instance.hint)

  def test_initialize__inheritance(
      self,
      assert_equal_instance: AssertEqual,
  ) -> None:
    assert_operation_inheritance(
        assert_equal_instance,
        bases=(AssertionBase, AssertEqual),
    )

  @pytest.mark.parametrize(
      "scenario",
      [
          CaseSensitivityScenario(sensitive=False, text="#!/usr/bin/Make -f"),
          CaseSensitivityScenario(sensitive=True, text="#!/usr/bin/make -f"),
      ],
  )
  def test_apply__vary_case_sensitivity__matches__stores_result(
      self,
      assert_equal_instance: AssertEqual,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
      scenario: CaseSensitivityScenario,
  ) -> None:
    mocked_textfile.__next__.return_value = scenario.text
    assert_equal_instance.case_sensitive = scenario.sensitive
    expected_split_text = scenario.text.split("/")

    assert_equal_instance.apply(mocked_controller)

    assert len(mocked_controller.forest.add.mock_calls) == 1
    result_tree = mocked_controller.forest.add.mock_calls[0].args[0]
    assert_result_tree(
        result_tree,
        assert_equal_instance.save,
        [expected_split_text],
    )

  @pytest.mark.parametrize(
      "scenario",
      [
          CaseSensitivityScenario(sensitive=False, text="#!/bin/bash"),
          CaseSensitivityScenario(sensitive=True, text="#!/usr/bin/Make -f"),
      ],
  )
  def test_apply__vary_case_sensitivity__does_not_match__raises_exception(
      self,
      assert_equal_instance: AssertEqual,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
      scenario: CaseSensitivityScenario,
  ) -> None:
    mocked_textfile.index = 1
    mocked_textfile.__next__.return_value = scenario.text
    assert_equal_instance.case_sensitive = scenario.sensitive

    with pytest.raises(AssertionViolation) as exc:
      assert_equal_instance.apply(mocked_controller)

    mocked_controller.forest.add.assert_not_called()
    assert_is_assertion_violation(
        exc=exc,
        assertion=assert_equal_instance,
        textfile=mocked_textfile,
        expected=assert_equal_instance.expected,
    )
