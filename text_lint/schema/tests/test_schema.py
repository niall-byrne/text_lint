"""Test the Schema class."""

import json
import os
from io import StringIO
from typing import Any, Dict, Type
from unittest import mock

import pytest
from text_lint import config
from text_lint.__helpers__.schema import assert_is_schema_error
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.schema import SchemaError, UnsupportedSchemaVersion
from text_lint.version import version_tuple_to_string
from .. import Schema
from ..settings import SchemaSettings
from .fixtures import schemas


class TestSchema:
  """Test the Schema class."""

  @pytest.mark.parametrize("interpolate", [True, False])
  def test_initialize__attributes(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      interpolate: bool,
  ) -> None:
    mocked_file_handle.write(json.dumps(schemas.one_simple_assertion))
    mocked_file_handle.seek(0)

    instance = schema_class(mocked_schema_file, interpolate)

    assert instance.path == mocked_schema_file
    assert instance.version == (0, 5, 0)

  def test_initialize__interpolated__uses_env_vars(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
  ) -> None:
    mocked_file_handle.write(
        json.dumps(schemas.one_simple_assertion_interpolated)
    )
    mocked_file_handle.seek(0)

    with mock.patch.dict(
        os.environ,
        {
            "ENV_VAR": "0.6.0",
        },
        clear=True,
    ):
      instance = schema_class(mocked_schema_file, True)

    assert instance.version == (0, 6, 0)

  def test_initialize__translations(
      self,
      schema_class: Type[Schema],
  ) -> None:
    assert_is_translated(schema_class.msg_fmt_no_assertions)
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
    mocked_file_handle.write(json.dumps(schemas.one_simple_assertion))
    mocked_file_handle.seek(0)

    instance = schema_class(mocked_schema_file, False)

    assert isinstance(
        instance.settings,
        SchemaSettings,
    )
    assert instance.settings.comment_regex == (
        schemas.one_simple_assertion["settings"]["comment_regex"]
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
      schema_class(mocked_schema_file, False)

    assert_is_schema_error(
        exc=exc,
        description_t=(Schema.msg_fmt_invalid_schema_version,),
        schema_path=mocked_schema_file,
    )

  @pytest.mark.parametrize("supported_version", ["0.5.0", "0.7.0"])
  def test_initialize__supported_version__raises_no_exception(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      supported_version: str,
  ) -> None:
    schema = dict(schemas.one_simple_assertion)
    schema["version"] = supported_version
    mocked_file_handle.write(json.dumps(schema))
    mocked_file_handle.seek(0)

    schema_class(mocked_schema_file, False)

  @pytest.mark.parametrize("unsupported_version", ["0.0.1", "1.0.0"])
  def test_initialize__unsupported_version__raises_exception(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      unsupported_version: str,
  ) -> None:
    schema = dict(schemas.one_simple_assertion)
    schema["version"] = unsupported_version
    mocked_file_handle.write(json.dumps(schema))
    mocked_file_handle.seek(0)

    with pytest.raises(UnsupportedSchemaVersion) as exc:
      schema_class(mocked_schema_file, False)

    assert str(
        exc.value
    ) == UnsupportedSchemaVersion.msg_fmt_unsupported.format(
        version_tuple_to_string(config.MINIMUM_SUPPORTED_SCHEMA_VERSION),
        version_tuple_to_string(config.MAXIMUM_SUPPORTED_SCHEMA_VERSION),
    )
    assert_is_translated(UnsupportedSchemaVersion.msg_fmt_unsupported)

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
      schema_class(mocked_schema_file, False)

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
      schema_class(mocked_schema_file, False)

    assert_is_schema_error(
        exc=exc,
        description_t=(Schema.msg_fmt_invalid_settings_regex,),
        schema_path=mocked_schema_file,
    )

  @pytest.mark.parametrize(
      "invalid_schema", [schemas.schema_missing_assertions]
  )
  def test_load_assertions__missing_assertions__raises_exception(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      invalid_schema: Dict[str, Any],
  ) -> None:
    mocked_file_handle.write(json.dumps(invalid_schema))
    mocked_file_handle.seek(0)
    instance = schema_class(mocked_schema_file, False)

    with pytest.raises(SchemaError) as exc:
      instance.load_assertions()

    assert_is_schema_error(
        exc=exc,
        description_t=(Schema.msg_fmt_no_assertions,),
        schema_path=mocked_schema_file,
    )

  @pytest.mark.parametrize("invalid_schema", [schemas.schema_empty_assertions])
  def test_load_assertions__empty_assertions__raises_exception(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      invalid_schema: Dict[str, Any],
  ) -> None:
    mocked_file_handle.write(json.dumps(invalid_schema))
    mocked_file_handle.seek(0)
    instance = schema_class(mocked_schema_file, False)

    with pytest.raises(SchemaError) as exc:
      instance.load_assertions()

    assert_is_schema_error(
        exc=exc,
        description_t=(Schema.msg_fmt_no_assertions,),
        schema_path=mocked_schema_file,
    )

  def test_load_assertions__returns_assertions_schema_section_content(
      self,
      schema_class: Type[Schema],
      mocked_file_handle: StringIO,
      mocked_schema_file: str,
      mocked_schema_assertions_section: mock.Mock,
  ) -> None:
    mocked_file_handle.write(json.dumps(schemas.one_simple_assertion))
    mocked_file_handle.seek(0)
    instance = schema_class(mocked_schema_file, False)

    created_assertions = instance.load_assertions()

    assert created_assertions == (
        mocked_schema_assertions_section.return_value.load.return_value
    )
    mocked_schema_assertions_section.return_value.load.assert_called_once_with(
        schemas.one_simple_assertion["assertions"]
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
    instance = schema_class(mocked_schema_file, False)

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
    mocked_file_handle.write(json.dumps(schemas.one_simple_assertion))
    mocked_file_handle.seek(0)
    instance = schema_class(mocked_schema_file, False)

    created_validators = instance.load_validators()

    assert created_validators == (
        mocked_schema_validators_section.return_value.load.return_value
    )
    mocked_schema_validators_section.return_value.load.assert_called_once_with(
        schemas.one_simple_assertion["validators"]
    )
