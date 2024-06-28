"""Logging context managers."""

from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator

from text_lint.config import LOGGING_COLUMN1_WIDTH
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # no cover
  from text_lint.linter import Linter
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )
  from text_lint.operations.validators.bases.validator_base import (
      ValidatorBase,
  )


msg_log_filename_text_file = _("file:")
msg_log_filename_schema = _("schema:")
msg_log_section_assertions = _("assertions")
msg_log_section_end = _("text_lint complete")
msg_log_section_start = _("text_lint start")
msg_log_section_validators = _("validators")


@contextmanager
def main(linter: "Linter") -> Generator[None, None, None]:
  linter.log(
      msg_log_section_start,
      indent=False,
      section=True,
  )
  linter.log(
      msg_log_filename_text_file.ljust(LOGGING_COLUMN1_WIDTH) +
      linter.settings.file_path,
      indent=False,
      section=False,
  )
  linter.log(
      msg_log_filename_schema.ljust(LOGGING_COLUMN1_WIDTH) +
      linter.settings.schema_path,
      indent=False,
      section=False,
  )
  yield None
  linter.log(
      msg_log_section_end,
      indent=False,
      section=True,
  )


@contextmanager
def assertion(
    linter: "Linter",
    operation: "AssertionBase",
) -> Generator[None, None, None]:
  start_index = linter.textfile.index
  yield None
  linter.log(
      operation,
      index=start_index,
  )


@contextmanager
def assertion_section(linter: "Linter") -> Generator[None, None, None]:
  linter.log(
      msg_log_section_assertions,
      indent=False,
      section=True,
  )
  yield None


@contextmanager
def validator(
    linter: "Linter",
    operation: "ValidatorBase",
) -> Generator[None, None, None]:
  linter.log(operation)
  yield None


@contextmanager
def validator_section(linter: "Linter") -> Generator[None, None, None]:
  linter.log(
      msg_log_section_validators,
      indent=False,
      section=True,
  )
  yield None
