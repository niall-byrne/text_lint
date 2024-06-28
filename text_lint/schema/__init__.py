"""Schema class."""

import re
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, cast

import yaml
from text_lint.exceptions.schema import SchemaError
from text_lint.schema.assertions import SchemaAssertions
from text_lint.schema.settings import SchemaSettings
from text_lint.schema.validators import SchemaValidators
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )
  from text_lint.operations.validators.bases.validator_base import (
      ValidatorBase,
  )
  from text_lint.schema.bases.section_base import AliasYamlOperation


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
    self.version: Tuple[int, ...] = self._parse_schema_version()
    self.settings = self._parse_schema_settings()
    self._assertions = SchemaAssertions(self)
    self._validators = SchemaValidators(self)

  def load_assertions(self) -> List["AssertionBase"]:
    """Create and return the text file parser assertion operation instances."""
    return self._assertions.load(self._parse_schema_assertions())

  def _parse_schema_assertions(self) -> List["AliasYamlOperation"]:
    try:
      return cast(List[Dict[str, Any]], self._content["assertions"])
    except KeyError as exc:
      raise self.create_exception(
          description=f(self.msg_fmt_no_assertions, nl=1),
      ) from exc

  def load_validators(self) -> List["ValidatorBase"]:
    """Create and return the text file parser validation instances."""
    return self._validators.load(self._parse_schema_validators())

  def _parse_schema_validators(self) -> List["AliasYamlOperation"]:
    try:
      return cast(List[Dict[str, Any]], self._content["validators"])
    except KeyError as exc:
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

  def _parse_schema_version(self) -> Tuple[int, ...]:
    try:
      return tuple(map(int, (self._content["version"].split("."))))
    except (KeyError, ValueError) as exc:
      raise self.create_exception(
          description=f(self.msg_fmt_invalid_schema_version, nl=1)
      ) from exc

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
