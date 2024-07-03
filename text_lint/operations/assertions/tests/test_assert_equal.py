"""Test AssertEqual class."""

from unittest import mock

import pytest
from text_lint.__helpers__.assertion import (
    assert_assertion_attributes,
    assert_state_saved,
)
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from ..assert_equal import YAML_EXAMPLE, AssertEqual
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
        "yaml_example": YAML_EXAMPLE,
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
        "yaml_example": YAML_EXAMPLE,
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
  def test_apply__vary_case_sensitivity__matches__saves_result(
      self,
      assert_equal_instance: AssertEqual,
      mocked_state: mock.Mock,
      scenario: CaseSensitivityScenario,
  ) -> None:
    mocked_state.next.return_value = scenario.text
    assert_equal_instance.case_sensitive = scenario.sensitive

    assert_equal_instance.apply(mocked_state)

    assert_state_saved(
        assert_equal_instance,
        mocked_state,
        [scenario.text],
    )

  @pytest.mark.parametrize(
      "scenario",
      [
          CaseSensitivityScenario(sensitive=False, text="#!/bin/bash"),
          CaseSensitivityScenario(sensitive=True, text="#!/usr/bin/Make -f"),
      ],
  )
  def test_apply__vary_case_sensitivity__does_not_match__calls_fail(
      self,
      assert_equal_instance: AssertEqual,
      mocked_state: mock.Mock,
      scenario: CaseSensitivityScenario,
  ) -> None:
    mocked_state.next.return_value = scenario.text
    assert_equal_instance.case_sensitive = scenario.sensitive

    assert_equal_instance.apply(mocked_state)

    mocked_state.fail.assert_called_once_with(assert_equal_instance.expected)
