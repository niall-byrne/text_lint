"""Test the Schema class."""

import json
from io import StringIO
from typing import Any, Dict, Type
from unittest import mock

import pytest
from text_lint.__helpers__.schema import assert_is_schema_error
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.schema import SchemaError
from .. import Schema
from ..settings import SchemaSettings
from .fixtures import schemas


class TestSchema:
  """Test the Schema class."""

  def test_initialize__attributes(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
  ) -> None:
    mocked_file_handle.write(json.dumps(schemas.one_simple_rule))
    mocked_file_handle.seek(0)

    instance = schema_class(mocked_schema_file)

    assert instance.path == mocked_schema_file
    assert instance.version == (0, 1, 0)

  def test_initialize__translations(
      self,
      schema_class: Type[Schema],
  ) -> None:
    assert_is_translated(schema_class.msg_fmt_no_rules)
    assert_is_translated(schema_class.msg_fmt_no_validators)
    assert_is_translated(schema_class.msg_fmt_invalid_settings)
    assert_is_translated(schema_class.msg_fmt_invalid_settings_regex)
    assert_is_translated(schema_class.msg_fmt_invalid_schema_version)

  def test_initialize__settings(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
  ) -> None:
    mocked_file_handle.write(json.dumps(schemas.one_simple_rule))
    mocked_file_handle.seek(0)

    instance = schema_class(mocked_schema_file)

    assert isinstance(
        instance.settings,
        SchemaSettings,
    )
    assert instance.settings.comment_regex == (
        schemas.one_simple_rule["settings"]["comment_regex"]
    )

  @pytest.mark.parametrize(
      "invalid_schema",
      [
          schemas.schema_missing_version,
          schemas.schema_invalid_version,
      ],
  )
  def test_initialize__missing_or_invalid_version__raises_exception(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      invalid_schema: Dict[str, Any],
  ) -> None:
    mocked_file_handle.write(json.dumps(invalid_schema))
    mocked_file_handle.seek(0)

    with pytest.raises(SchemaError) as exc:
      schema_class(mocked_schema_file)

    assert_is_schema_error(
        exc=exc,
        description_t=(Schema.msg_fmt_invalid_schema_version,),
        schema_path=mocked_schema_file,
    )

  @pytest.mark.parametrize(
      "invalid_schema",
      [
          schemas.schema_invalid_settings,
          schemas.schema_extra_settings,
      ],
  )
  def test_initialize__invalid_settings__raises_exception(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      invalid_schema: Dict[str, Any],
  ) -> None:
    mocked_file_handle.write(json.dumps(invalid_schema))
    mocked_file_handle.seek(0)

    with pytest.raises(SchemaError) as exc:
      schema_class(mocked_schema_file)

    assert_is_schema_error(
        exc=exc,
        description_t=(Schema.msg_fmt_invalid_settings,),
        schema_path=mocked_schema_file,
    )

  @pytest.mark.parametrize(
      "invalid_schema",
      [
          schemas.schema_settings_invalid_regex,
      ],
  )
  def test_initialize__invalid_regex_in_settings__raises_exception(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      invalid_schema: Dict[str, Any],
  ) -> None:
    mocked_file_handle.write(json.dumps(invalid_schema))
    mocked_file_handle.seek(0)

    with pytest.raises(SchemaError) as exc:
      schema_class(mocked_schema_file)

    assert_is_schema_error(
        exc=exc,
        description_t=(Schema.msg_fmt_invalid_settings_regex,),
        schema_path=mocked_schema_file,
    )

  @pytest.mark.parametrize("invalid_schema", [schemas.schema_missing_rules])
  def test_load_rules__missing_rules__raises_exception(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      invalid_schema: Dict[str, Any],
  ) -> None:
    mocked_file_handle.write(json.dumps(invalid_schema))
    mocked_file_handle.seek(0)
    instance = schema_class(mocked_schema_file)

    with pytest.raises(SchemaError) as exc:
      instance.load_rules()

    assert_is_schema_error(
        exc=exc,
        description_t=(Schema.msg_fmt_no_rules,),
        schema_path=mocked_schema_file,
    )

  @pytest.mark.parametrize("invalid_schema", [schemas.schema_empty_rules])
  def test_load_rules__empty_rules__raises_exception(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      invalid_schema: Dict[str, Any],
  ) -> None:
    mocked_file_handle.write(json.dumps(invalid_schema))
    mocked_file_handle.seek(0)
    instance = schema_class(mocked_schema_file)

    with pytest.raises(SchemaError) as exc:
      instance.load_rules()

    assert_is_schema_error(
        exc=exc,
        description_t=(Schema.msg_fmt_no_rules,),
        schema_path=mocked_schema_file,
    )

  def test_load_rules__returns_rule_schema_section_content(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      mocked_schema_rules_section: mock.Mock,
  ) -> None:
    mocked_file_handle.write(json.dumps(schemas.one_simple_rule))
    mocked_file_handle.seek(0)
    instance = schema_class(mocked_schema_file)

    created_rules = instance.load_rules()

    assert created_rules == (
        mocked_schema_rules_section.return_value.load.return_value
    )
    mocked_schema_rules_section.return_value.load.assert_called_once_with(
        schemas.one_simple_rule["rules"]
    )

  @pytest.mark.parametrize(
      "invalid_schema", [schemas.schema_missing_validators]
  )
  def test_load_validators__missing_validators__raises_exception(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      invalid_schema: Dict[str, Any],
  ) -> None:
    mocked_file_handle.write(json.dumps(invalid_schema))
    mocked_file_handle.seek(0)
    instance = schema_class(mocked_schema_file)

    with pytest.raises(SchemaError) as exc:
      instance.load_validators()

    assert_is_schema_error(
        exc=exc,
        description_t=(Schema.msg_fmt_no_validators,),
        schema_path=mocked_schema_file,
    )

  def test_load_validators__returns_validator_schema_section_content(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      mocked_schema_validators_section: mock.Mock,
  ) -> None:
    mocked_file_handle.write(json.dumps(schemas.one_simple_rule))
    mocked_file_handle.seek(0)
    instance = schema_class(mocked_schema_file)

    created_validators = instance.load_validators()

    assert created_validators == (
        mocked_schema_validators_section.return_value.load.return_value
    )
    mocked_schema_validators_section.return_value.load.assert_called_once_with(
        schemas.one_simple_rule["validators"]
    )
