"""Test the AssertionRegexBase class."""

from typing import Type
from unittest import mock

from text_lint.__helpers__.assertion import assert_assertion_attributes
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
    assert_parameter_schema,
    spy_on_validate_parameters,
)
from text_lint.config import SAVED_NAME_REGEX
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.assertions.bases.assertion_regex_base import (
    AssertionRegexBase,
)
from text_lint.operations.mixins.parameter_validation import validators


class TestAssertionRegexBase:
  """Test the AssertionRegexBase class."""

  def test_intialize__defaults__attributes(
      self,
      concrete_assertion_regex_base_class: Type[AssertionRegexBase],
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "a concrete regex hint",
        "internal_use_only": False,
        "name": "concrete name",
        "operation": concrete_assertion_regex_base_class.operation,
        "regex": r'(.*).py',
        "save": None,
        "splits": {},
        "yaml_example": "mocked_yaml_example_assertion_regex",
    }

    instance = concrete_assertion_regex_base_class(
        name="concrete name", regex=r'(.*).py'
    )

    assert_assertion_attributes(instance, attributes)

  def test_initialize__defined__attributes(
      self,
      concrete_assertion_regex_base_class: Type[AssertionRegexBase],
      concrete_assertion_regex_base_instance: AssertionRegexBase,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "a concrete regex hint",
        "internal_use_only": False,
        "name": "concrete name",
        "operation": concrete_assertion_regex_base_class.operation,
        "regex": r'[a-z]+',
        "save": "save_id",
        "splits": {
            1: None
        },
        "yaml_example": "mocked_yaml_example_assertion_regex",
    }

    assert_assertion_attributes(
        concrete_assertion_regex_base_instance, attributes
    )

  def test_initialize__inheritance(
      self,
      concrete_assertion_regex_base_instance: AssertionRegexBase,
  ) -> None:
    assert_operation_inheritance(
        concrete_assertion_regex_base_instance,
        bases=(AssertionBase, AssertionRegexBase),
    )

  @spy_on_validate_parameters(AssertionRegexBase)
  def test_initialize__parameter_validation(
      self,
      validate_parameters_spy: mock.Mock,
      concrete_assertion_regex_base_instance: AssertionRegexBase,
  ) -> None:
    assert_parameter_schema(
        # pylint: disable=duplicate-code
        instance=concrete_assertion_regex_base_instance,
        parameter_definitions={
            "name": {
                "type": str
            },
            "save":
                {
                    "type":
                        str,
                    "optional":
                        True,
                    "validators":
                        [validators.create_matches_regex(SAVED_NAME_REGEX)],
                }
        }
    )
    validate_parameters_spy.assert_called_once_with(
        concrete_assertion_regex_base_instance
    )
