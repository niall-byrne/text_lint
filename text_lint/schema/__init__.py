"""Schema class."""

import re
from typing import TYPE_CHECKING, List, Optional, Tuple

import yaml
from text_lint.exceptions.schema import SchemaError
from text_lint.schema.rules import SchemaRules
from text_lint.schema.settings import SchemaSettings
from text_lint.schema.validators import SchemaValidators
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.rules.bases.rule_base import RuleBase
  from text_lint.operations.validators.bases.validator_base import (
      ValidationBase,
  )
  from text_lint.schema.bases.section_base import AliasYamlOperation


class Schema:
  """A text file schema file."""

  msg_fmt_no_rules = _("no rules found in schema")
  msg_fmt_no_validators = _("no validators found in schema")
  msg_fmt_invalid_settings = _("invalid schema settings")
  msg_fmt_invalid_settings_regex = _("invalid regex in schema settings")
  msg_fmt_invalid_schema_version = _("invalid schema version")

  def __init__(self, schema_path: str) -> None:
    self.path = schema_path
    with open(self.path, 'r', encoding="utf-8") as file_handle:
      self._content = yaml.safe_load(file_handle)
    self.version: Tuple[int, ...] = self._parse_schema_version()
    self.settings = self._parse_schema_settings()
    self._rules = SchemaRules(self)
    self._validators = SchemaValidators(self)

  def load_rules(self) -> List["RuleBase"]:
    """Create and return the text file parser rule operation instances."""
    return self._rules.load(self._parse_schema_rules())

  def _parse_schema_rules(self) -> List["AliasYamlOperation"]:
    try:
      schema_rules = self._content["rules"]
      assert isinstance(schema_rules, list)
      return schema_rules
    except (KeyError, AssertionError) as exc:
      raise self.create_exception(
          description=f(self.msg_fmt_no_rules, nl=1),
      ) from exc

  def load_validators(self) -> List["ValidationBase"]:
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
