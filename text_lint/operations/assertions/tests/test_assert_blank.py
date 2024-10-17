"""Test AssertBlank class."""

from unittest import mock

from text_lint.__helpers__.assertion import assert_assertion_attributes
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
from ..assert_blank import YAML_EXAMPLE, YAML_EXAMPLE_COMPONENTS, AssertBlank


class TestAssertBlank:
  """Test the AssertBlank class."""

  def test_initialize__defined__attributes(
      self,
      assert_blank_instance: AssertBlank,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "the line contains no text",
        "internal_use_only": False,
        "name": "example assert blank assertion",
        "operation": "assert_blank",
        "save": None,
        "splits": {},
        "yaml_example": YAML_EXAMPLE,
    }

    assert_assertion_attributes(assert_blank_instance, attributes)

  def test_initialize__translations(
      self,
      assert_blank_instance: AssertBlank,
  ) -> None:
    assert_is_translated(assert_blank_instance.hint)
    assert_is_translated_yaml_example(
        assert_blank_instance.yaml_example,
        YAML_EXAMPLE_COMPONENTS,
    )

  def test_initialize__inheritance(
      self,
      assert_blank_instance: AssertBlank,
  ) -> None:
    assert_operation_inheritance(
        assert_blank_instance,
        bases=(AssertionBase, AssertBlank),
    )

  @spy_on_validate_parameters(AssertBlank)
  def test_initialize__parameter_validation(
      self,
      validate_parameters_spy: mock.Mock,
      assert_blank_instance: AssertBlank,
      base_parameter_definitions: AliasParameterDefinitions,
  ) -> None:
    del base_parameter_definitions["save"]

    assert_parameter_schema(
        instance=assert_blank_instance,
        parameter_definitions=base_parameter_definitions,
    )
    validate_parameters_spy.assert_called_once_with(assert_blank_instance)

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
