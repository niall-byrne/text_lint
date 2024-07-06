"""Test the SchemaSectionBase class."""

import re
from copy import deepcopy
from typing import Dict, Type
from unittest import mock

import pytest
from text_lint.__helpers__.schema import assert_is_schema_error
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.schema import SchemaError
from ..section_base import SchemaSectionBase
from .fixtures import schemas


class TestSchemaSectionBase:
  """Test the SchemaSectionBase class."""

  def test_initialize__attributes(
      self,
      concrete_schema_section_instance: SchemaSectionBase[mock.Mock],
      mocked_operation_classes: Dict[str, Type[mock.Mock]],
  ) -> None:
    assert concrete_schema_section_instance.operation_classes == (
        mocked_operation_classes
    )
    assert concrete_schema_section_instance.entity_name == "mocked_entity"

  def test_initialize__translations(
      self,
      concrete_schema_section_instance: SchemaSectionBase[mock.Mock],
  ) -> None:
    assert_is_translated(
        concrete_schema_section_instance.msg_fmt_unknown_operation
    )
    assert_is_translated(
        concrete_schema_section_instance.msg_fmt_unknown_syntax
    )
    assert_is_translated(concrete_schema_section_instance.msg_fmt_invalid_regex)

  def test_load__defined_section__returns_expected_instance(
      self,
      concrete_schema_section_instance: SchemaSectionBase[mock.Mock],
      mocked_operation_classes: Dict[str, mock.Mock],
  ) -> None:
    instances = concrete_schema_section_instance.load(
        deepcopy(schemas.one_simple_rule)
    )

    assert len(instances) == 1
    assert instances[0].operation == schemas.one_simple_rule[0]["operation"]
    mocked_operation_classes[instances[0].operation].assert_called_once_with(
        name=schemas.one_simple_rule[0]["name"]
    )

  def test_load__defined_section__calls_overridable_hooks(
      self,
      concrete_schema_section_instance: SchemaSectionBase[mock.Mock],
      mocked_create_operation_instance_hook: mock.Mock,
      mocked_load_operation_instances_hook: mock.Mock,
      mocked_operation_classes: Dict[str, Type[mock.Mock]],
  ) -> None:
    cloned_schema = deepcopy(schemas.two_simple_rules)

    instances = concrete_schema_section_instance.load(cloned_schema)

    mocked_load_operation_instances_hook.assert_called_once_with(
        instances,
        cloned_schema,
    )
    assert mocked_create_operation_instance_hook.mock_calls == [
        mock.call(
            mocked_operation_classes[schemas.two_simple_rules[index]
                                     ["operation"]],
            cloned_schema[index],
        ) for index in range(0, len(cloned_schema))
    ]

  @pytest.mark.parametrize(
      "invalid_schema_rules",
      [
          schemas.invalid_operation,
      ],
  )
  def test_load__defined_section__invalid_operation__raises_schema_exception(
      self,
      concrete_schema_section_instance: SchemaSectionBase[mock.Mock],
      mocked_schema: mock.Mock,
      invalid_schema_rules: schemas.AliasRawSchemaRules,
  ) -> None:
    with pytest.raises(SchemaError) as exc:
      concrete_schema_section_instance.load(deepcopy(invalid_schema_rules))

    assert_is_schema_error(
        exc=exc,
        description_t=(
            concrete_schema_section_instance.msg_fmt_unknown_operation,
            concrete_schema_section_instance.entity_name,
            1,
        ),
        rule_definition=invalid_schema_rules[0],
        schema_path=mocked_schema.path,
    )

  @pytest.mark.parametrize("exception", [AttributeError, KeyError, TypeError])
  def test_load__defined_section__vary_exception__raises_schema_exception(
      self,
      concrete_schema_section_instance: SchemaSectionBase[mock.Mock],
      mocked_operation_classes: Dict[str, Type[mock.Mock]],
      mocked_schema: mock.Mock,
      exception: Type[Exception],
  ) -> None:
    mocked_operation_classes["A"].side_effect = exception("exception")
    cloned_schema = deepcopy(schemas.one_simple_rule)

    with pytest.raises(SchemaError) as exc:
      concrete_schema_section_instance.load(cloned_schema)

    assert_is_schema_error(
        exc=exc,
        description_t=(
            concrete_schema_section_instance.msg_fmt_unknown_syntax,
            concrete_schema_section_instance.entity_name,
            1,
        ),
        rule_definition=cloned_schema[0],
        schema_path=mocked_schema.path,
    )

  @pytest.mark.parametrize("exception", [re.error])
  def test_load__defined_section__regex_exception__raises_schema_exception(
      self,
      concrete_schema_section_instance: SchemaSectionBase[mock.Mock],
      mocked_operation_classes: Dict[str, Type[mock.Mock]],
      mocked_schema: mock.Mock,
      exception: Type[Exception],
  ) -> None:
    mocked_operation_classes["A"].side_effect = exception("error")
    cloned_schema = deepcopy(schemas.one_simple_rule)

    with pytest.raises(SchemaError) as exc:
      concrete_schema_section_instance.load(cloned_schema)

    assert_is_schema_error(
        exc=exc,
        description_t=(
            concrete_schema_section_instance.msg_fmt_invalid_regex,
            concrete_schema_section_instance.entity_name,
            1,
        ),
        rule_definition=cloned_schema[0],
        schema_path=mocked_schema.path,
    )
