"""Test AssertRegex class."""

from unittest import mock

from text_lint.__helpers__.assertion import (
    assert_assertion_attributes,
    assert_state_saved,
)
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    AliasParameterDefinitions,
    assert_operation_inheritance,
    assert_parameter_schema,
    spy_on_validate_parameters,
)
from text_lint.__helpers__.translations import (
    assert_is_translated,
    assert_is_translated_yaml_example,
)
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.assertions.bases.assertion_regex_base import (
    AssertionRegexBase,
)
from ..assert_regex import YAML_EXAMPLE, YAML_EXAMPLE_COMPONENTS, AssertRegex


class TestAssertRegex:
  """Test the AssertRegex class."""

  def test_initialize__defaults__attributes(self) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "this line must match the regex",
        "internal_use_only": False,
        "name": "example assert regex assertion",
        "operation": "assert_regex",
        "regex": "^([a-z-]+):\\s.+$",
        "save": None,
        "splits": {},
        "yaml_example": YAML_EXAMPLE,
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
        "internal_use_only": False,
        "name": "example assert regex assertion",
        "operation": "assert_regex",
        "regex": "^([a-z-]+):\\s.+$",
        "save": "example",
        "splits": {
            1: " "
        },
        "yaml_example": YAML_EXAMPLE,
    }

    assert_assertion_attributes(assert_regex_instance, attributes)

  def test_initialize__translations(
      self,
      assert_regex_instance: AssertRegex,
  ) -> None:
    assert_is_translated(assert_regex_instance.hint)
    assert_is_translated_yaml_example(
        assert_regex_instance.yaml_example,
        YAML_EXAMPLE_COMPONENTS,
        assertion_options=True,
    )

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

  @spy_on_validate_parameters(AssertRegex)
  def test_initialize__parameter_validation(
      self,
      validate_parameters_spy: mock.Mock,
      assert_regex_instance: AssertRegex,
      base_parameter_definitions: AliasParameterDefinitions,
  ) -> None:
    assert_parameter_schema(
        instance=assert_regex_instance,
        parameter_definitions=base_parameter_definitions,
    )
    validate_parameters_spy.assert_called_once_with(assert_regex_instance)

  def test_apply__matches__saves_result(
      self,
      assert_regex_instance: AssertRegex,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.next.return_value = "matching: string"

    assert_regex_instance.apply(mocked_state)

    assert_state_saved(
        assert_regex_instance,
        mocked_state,
        [mocked_state.next.return_value],
    )

  def test_apply__does_not_match__calls_fail(
      self,
      assert_regex_instance: AssertRegex,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.next.return_value = "non matching string"

    assert_regex_instance.apply(mocked_state)

    mocked_state.fail.assert_called_once_with(
        assert_regex_instance.regex.pattern
    )
