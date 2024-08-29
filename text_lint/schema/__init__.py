"""Schema class."""

import re
from typing import TYPE_CHECKING, List, Optional

import yaml
from text_lint import config
from text_lint.exceptions.schema import SchemaError, UnsupportedSchemaVersion
from text_lint.schema.assertions import SchemaAssertions
from text_lint.schema.settings import SchemaSettings
from text_lint.schema.validators import SchemaValidators
from text_lint.utilities.translations import _, f
from text_lint.version import string_to_version_tuple

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )
  from text_lint.operations.validators.bases.validator_base import (
      ValidatorBase,
  )
  from text_lint.schema.bases.section_base import AliasYamlOperation
  from text_lint.version import AliasVersionTuple


class Schema:
  """A text file schema file."""

  msg_fmt_no_assertions = _("No assertions found in schema")
  msg_fmt_no_validators = _("No validators found in schema")
  msg_fmt_invalid_settings = _("Invalid schema settings")
  msg_fmt_invalid_settings_regex = _("Invalid regex in schema settings")
  msg_fmt_invalid_schema_version = _("Invalid schema version")

  def __init__(self, schema_path: str) -> None:
    self.path = schema_path
    with open(self.path, 'r', encoding="utf-8") as file_handle:
      self._content = yaml.safe_load(file_handle)
    self.version: "AliasVersionTuple" = self._parse_schema_version()
    self.settings = self._parse_schema_settings()
    self._assertions = SchemaAssertions(self)
    self._validators = SchemaValidators(self)

  def load_assertions(self) -> List["AssertionBase"]:
    """Create and return the text file parser assertion operation instances."""
    return self._assertions.load(self._parse_schema_assertions())

  def _parse_schema_assertions(self) -> List["AliasYamlOperation"]:
    try:
      schema_assertions = self._content["assertions"]
      assert isinstance(schema_assertions, list)
      assert len(schema_assertions) > 0
      return schema_assertions
    except (KeyError, AssertionError) as exc:
      raise self.create_exception(
          description=f(self.msg_fmt_no_assertions, nl=1),
      ) from exc

  def load_validators(self) -> List["ValidatorBase"]:
    """Create and return the text file parser validation instances."""
    return self._validators.load(self._parse_schema_validators())

  def _parse_schema_validators(self) -> List["AliasYamlOperation"]:
    try:
      schema_validators = self._content["validators"]
      assert isinstance(schema_validators, list)
      return schema_validators
    except (KeyError, AssertionError) as exc:
      raise self.create_exception(
          description=f(self.msg_fmt_no_validators, nl=1),
      ) from exc

  def _parse_schema_settings(self) -> SchemaSettings:
    if "settings" in self._content:
      try:
        return SchemaSettings(**self._content["settings"])
      except (KeyError, TypeError) as exc:
        raise self.create_exception(
            description=f(self.msg_fmt_invalid_settings, nl=1)
        ) from exc
      except re.error as exc:
        raise self.create_exception(
            description=f(self.msg_fmt_invalid_settings_regex, nl=1)
        ) from exc
    return SchemaSettings(comment_regex=None)

  def _parse_schema_version(self) -> "AliasVersionTuple":
    try:
      version = string_to_version_tuple(self._content["version"])
    except (KeyError, ValueError) as exc:
      raise self.create_exception(
          description=f(self.msg_fmt_invalid_schema_version, nl=1)
      ) from exc
    self._validate_schema_version(version)
    return version

  def _validate_schema_version(self, version: "AliasVersionTuple") -> None:
    if (
        version < config.MINIMUM_SUPPORTED_SCHEMA_VERSION
        or version > config.MAXIMUM_SUPPORTED_SCHEMA_VERSION
    ):
      raise UnsupportedSchemaVersion()

  def create_exception(
      self,
      description: str,
      operation_definition: Optional["AliasYamlOperation"] = None,
  ) -> "SchemaError":
    return SchemaError(
        description=description,
        schema=self,
        operation_definition=operation_definition,
    )
