"""Test the SchemaRules class."""

from typing import TYPE_CHECKING, List
from unittest import mock

from text_lint.__fixtures__.mocks import AliasMethodMocker
from text_lint.__helpers__.translations import (
    as_translation,
    assert_is_translated,
)
from text_lint.operations.rules import (
    AssertSequenceBegins,
    AssertSequenceEnds,
    rule_registry,
)
from ..rules import SchemaRules
from .fixtures import schemas

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.rules.bases.rule_base import RuleBase
  from text_lint.schema import AliasYamlOperation


class TestSchemaRules:
  """Test the SchemaRules class."""

  def test_attributes(self) -> None:
    assert SchemaRules.automated_section_end_rule_name == as_translation(
        "Automated End of Section"
    )
    assert SchemaRules.operation_classes == rule_registry
    assert SchemaRules.entity_name == "rule"

  def test_translated_attributes(self,) -> None:
    assert_is_translated(SchemaRules.automated_section_end_rule_name)

  def test_hook_load_operation_instances__calls_schema_validator(
      self,
      mocked_operation_definitions: List["AliasYamlOperation"],
      mocked_operation_instances: List["RuleBase"],
      mocked_schema: mock.Mock,
  ) -> None:
    instance = SchemaRules(mocked_schema)

    instance.hook_load_operation_instances(
        mocked_operation_instances,
        mocked_operation_definitions,
    )

    for index, rule in enumerate(mocked_operation_instances):
      if isinstance(rule, mock.Mock):
        assert index < len(mocked_operation_instances) - 1
        rule.schema_validator.assert_called_once_with(
            index,
            mocked_operation_instances,
            mocked_operation_definitions,
            mocked_schema,
        )
      else:
        assert index == len(mocked_operation_instances) - 1
        assert isinstance(rule, AssertSequenceEnds)

  def test_hook_load_operation_instances__appends_assert_sequence_end(
      self,
      mocked_operation_definitions: List["AliasYamlOperation"],
      mocked_operation_instances: List["RuleBase"],
      mocked_schema: mock.Mock,
  ) -> None:
    instance = SchemaRules(mocked_schema)

    result = instance.hook_load_operation_instances(
        mocked_operation_instances,
        mocked_operation_definitions,
    )

    assert len(result) == 3
    assert result[0] == mocked_operation_instances[0]
    assert result[1] == mocked_operation_instances[1]
    assert isinstance(result[2], AssertSequenceEnds)
    assert result[2].name == SchemaRules.automated_section_end_rule_name

  def test_hook_create_operation_instance__nested_content__appends_nested_rules(
      self,
      mocked_schema: mock.Mock,
      method_mocker: AliasMethodMocker,
  ) -> None:
    mocked_operation_class = mock.Mock()
    mocked_operation_class.operation = AssertSequenceBegins.operation
    instance = SchemaRules(mocked_schema)
    mocked_load_method = method_mocker(instance.load)

    result = instance.hook_create_operation_instance(
        mocked_operation_class,
        {"rules": "mocked_yaml_content"},
    )

    assert result == {"rules": mocked_load_method.return_value}
    mocked_load_method.assert_called_once_with("mocked_yaml_content")

  def test_hook_create_operation_instance__non_nested_content__does_not_append(
      self,
      mocked_schema: mock.Mock,
      method_mocker: AliasMethodMocker,
  ) -> None:
    mocked_operation_class = mock.Mock()
    mocked_operation_class.operation = AssertSequenceEnds.operation
    instance = SchemaRules(mocked_schema)
    mocked_load_method = method_mocker(instance.load)

    result = instance.hook_create_operation_instance(
        mocked_operation_class,
        schemas.one_simple_rule["rules"][0],
    )

    assert result == schemas.one_simple_rule["rules"][0]
    mocked_load_method.assert_not_called()
