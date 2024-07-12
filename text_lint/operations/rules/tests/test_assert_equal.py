"""Test AssertEqual class."""

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
from ..assert_equal import YAML_EXAMPLE, AssertEqual
from .conftest import CaseSensitivityScenario


class TestAssertEqual:
  """Test the AssertEqual class."""

  def test_initialize__defaults__attributes(self) -> None:
    attributes: AliasOperationAttributes = {
        "case_sensitive": True,
        "expected": "#!/usr/bin/make -f\n",
        "hint": "this line must match the expected value",
        "internal_use_only": False,
        "matches": [],
        "name": "example assert equal rule",
        "operation": "assert_equal",
        "regex": "(.*)",
        "save": None,
        "splits": {},
        "yaml_example": YAML_EXAMPLE,
    }

    instance = AssertEqual(
        name="example assert equal rule",
        expected="#!/usr/bin/make -f\n",
    )

    assert_rule_attributes(instance, attributes)

  def test_initialize__defined__attributes(
      self,
      assert_equal_instance: AssertEqual,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "case_sensitive": False,
        "expected": "#!/usr/bin/make -f\n",
        "hint": "this line must match the expected value",
        "internal_use_only": False,
        "matches": [],
        "name": "example assert equal rule",
        "operation": "assert_equal",
        "regex": "(.*)",
        "save": "example",
        "splits": {
            1: "/"
        },
        "yaml_example": YAML_EXAMPLE,
    }

    assert_rule_attributes(assert_equal_instance, attributes)

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
        bases=(RuleBase, AssertEqual),
    )

  @pytest.mark.parametrize(
      "scenario",
      [
          CaseSensitivityScenario(sensitive=False, text="#!/usr/bin/Make -f\n"),
          CaseSensitivityScenario(sensitive=True, text="#!/usr/bin/make -f\n"),
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

    assert_equal_instance.apply(mocked_controller)

    assert len(assert_equal_instance.matches) == 1
    assert assert_equal_instance.matches[0].group(1) == scenario.text

  @pytest.mark.parametrize(
      "scenario",
      [
          CaseSensitivityScenario(sensitive=False, text="#!/bin/bash\n"),
          CaseSensitivityScenario(sensitive=True, text="#!/usr/bin/Make -f\n"),
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

    with pytest.raises(RuleViolation) as exc:
      assert_equal_instance.apply(mocked_controller)

    assert len(assert_equal_instance.matches) == 0
    assert_is_rule_violation(
        exc=exc,
        rule=assert_equal_instance,
        textfile=mocked_textfile,
        expected=assert_equal_instance.expected,
    )
