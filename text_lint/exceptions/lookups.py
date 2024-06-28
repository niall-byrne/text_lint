"""Exceptions for the text_lint result lookups."""
from typing import TYPE_CHECKING

from text_lint.utilities.translations import _, f
from text_lint.utilities.whitespace import make_visible

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.lookups.bases.lookup_base import LookupBase


class LookupExceptionBase(ValueError):
  """Base class for lookup exceptions."""


class LookupFailure(LookupExceptionBase):
  """Raised when a lookup operation fails."""

  msg_fmt_lookup_operation = _("  LOOKUP OPERATION: {0}")
  msg_fmt_schema_operation_name = _("  SCHEMA OPERATION NAME: {0}")
  msg_fmt_lookup_definition = _("  LOOKUP DEFINITION:")
  msg_fmt_result_source = _("    RESULT SOURCE: '{0}'")
  msg_fmt_lookups = _("    LOOKUPS: {0}")
  msg_fmt_failed_lookup = _("    FAILED LOOKUP: '{0}'")
  msg_fmt_hint = _("    HINT: '{0}'")

  def __init__(
      self,
      description: str,
      lookup: "LookupBase",
  ) -> None:
    message = description
    message += f(
        self.msg_fmt_lookup_operation,
        lookup.__class__.__name__,
        nl=1,
    )
    message += f(
        self.msg_fmt_schema_operation_name,
        make_visible(lookup.requesting_operation_name),
        nl=1,
    )
    message += f(
        self.msg_fmt_lookup_definition,
        nl=1,
    )
    message += f(
        self.msg_fmt_result_source,
        make_visible(lookup.result_set.source),
        nl=1,
    )
    message += f(
        self.msg_fmt_lookups,
        make_visible(lookup.result_set.lookups),
        nl=1,
    )
    message += f(
        self.msg_fmt_failed_lookup,
        make_visible(lookup.lookup_name),
        nl=1,
    )
    message += f(
        self.msg_fmt_hint,
        lookup.hint,
        nl=1,
    )

    super().__init__(message)


class LookupUnknown(LookupExceptionBase):
  """Raised when an unknown lookup is encountered."""

  msg_fmt_lookup_unknown_description = _(
      "Could not process this unknown lookup."
  )
  msg_fmt_lookup_operation = _("  LOOKUP OPERATION: {0}")
  msg_fmt_schema_operation_name = _("  SCHEMA OPERATION NAME: {0}")
  msg_fmt_lookup_definition = _("  LOOKUP DEFINITION:")
  msg_fmt_result_source = _("    RESULT SOURCE: '{0}'")
  msg_fmt_lookups = _("    LOOKUPS: {0}")
  msg_fmt_failed_lookup = _("    FAILED LOOKUP: '{0}'")
  msg_fmt_hint = _("    HINT: '{0}'")
  msg_fmt_lookup_unknown_hint = _(
      "to lookup a specific value, prefix the name with '{0}'"
  )

  def __init__(
      self,
      lookup: "LookupBase",
  ) -> None:
    message = f(
        self.msg_fmt_lookup_unknown_description,
        nl=1,
    )
    message += f(
        self.msg_fmt_lookup_operation,
        lookup.__class__.__name__,
        nl=1,
    )
    message += f(
        self.msg_fmt_schema_operation_name,
        make_visible(lookup.requesting_operation_name),
        nl=1,
    )
    message += f(
        self.msg_fmt_lookup_definition,
        nl=1,
    )
    message += f(
        self.msg_fmt_result_source,
        make_visible(lookup.result_set.source),
        nl=1,
    )
    message += f(
        self.msg_fmt_lookups,
        make_visible(lookup.result_set.lookups),
        nl=1,
    )
    message += f(
        self.msg_fmt_failed_lookup,
        make_visible(lookup.lookup_name),
        nl=1,
    )
    message += f(
        self.msg_fmt_hint,
        self.msg_fmt_lookup_unknown_hint,
        nl=1,
    )

    super().__init__(message)
