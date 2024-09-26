"""Exceptions for the text_lint schema."""
import os.path
from typing import TYPE_CHECKING, Any, Dict, Optional

from text_lint import config
from text_lint.utilities.translations import _, f
from text_lint.utilities.whitespace import make_visible
from text_lint.version import version_tuple_to_string

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.schema import Schema


class SchemaExceptionBase(ValueError):
  """Base class for schema exceptions."""


class SchemaError(SchemaExceptionBase):
  """Raised when a misconfiguration is found in the schema."""

  msg_fmt_schema_file = _("  SCHEMA FILE: {0}")
  msg_fmt_operation_definition = _("  OPERATION DEFINITION:")

  def __init__(
      self,
      description: str,
      schema: "Schema",
      operation_definition: Optional[Dict[str, Any]] = None,
  ) -> None:
    message = description
    message += f(
        self.msg_fmt_schema_file,
        os.path.abspath(schema.path),
        nl=1,
    )
    if operation_definition:
      message += f(
          self.msg_fmt_operation_definition,
          nl=1,
      )
      for key, value in operation_definition.items():
        message += "    {key}: {value}\n".format(
            key=key,
            value=make_visible(value),
        )
    super().__init__(message)


class LookupExpressionInvalid(SchemaExceptionBase):
  """Raised when a malformed lookup expression is found in the schema."""


class LookupExpressionInvalidDuplicatePositional(SchemaExceptionBase):
  """Raised when a positional lookup is used twice in an expression."""


class LookupExpressionInvalidSequence(SchemaExceptionBase):
  """Raised when a positional lookup is used after a transformation lookup."""


class SaveIdInvalid(SchemaExceptionBase):
  """Raised when a misconfigured save id is found in the schema."""


class SequenceInvalid(SchemaExceptionBase):
  """Raised when a misconfigured sequence control is found in the schema."""


class SplitGroupInvalid(SchemaExceptionBase):
  """Raised when a misconfigured split group is found in the schema."""


class UnsupportedSchemaVersion(SchemaExceptionBase):
  """Raised when a schema with an unsupported version is read."""

  msg_fmt_unsupported = _(
      "This version of text_lint only supports schema "
      "versions {0} through {1} !"
  )

  def __init__(self) -> None:
    super().__init__(
        self.msg_fmt_unsupported.format(
            version_tuple_to_string(config.MINIMUM_SUPPORTED_SCHEMA_VERSION),
            version_tuple_to_string(config.MAXIMUM_SUPPORTED_SCHEMA_VERSION),
        ),
    )
