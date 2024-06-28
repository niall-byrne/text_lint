"""Exceptions for the text_lint schema."""
import os.path
from typing import TYPE_CHECKING, Any, Dict, Optional

from text_lint.utilities.translations import _, f
from text_lint.utilities.whitespace import make_visible

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


class SequenceInvalid(SchemaExceptionBase):
  """Raised when a misconfigured sequence control is found in the schema."""


class SplitGroupInvalid(SchemaExceptionBase):
  """Raised when a misconfigured split group is found in the schema."""
