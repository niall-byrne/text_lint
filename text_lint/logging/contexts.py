"""Logging context managers."""

from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator

from text_lint.config import LOGGING_COLUMN1_WIDTH
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # no cover
  from text_lint.controller import Controller
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )
  from text_lint.operations.validators.bases.validator_base import (
      ValidationBase,
  )


msg_log_filename_text_file = _("file:")
msg_log_filename_schema = _("schema:")
msg_log_section_assertions = _("assertions")
msg_log_section_end = _("text_lint complete")
msg_log_section_start = _("text_lint start")
msg_log_section_validators = _("validators")


@contextmanager
def main(controller: "Controller") -> Generator[None, None, None]:
  controller.log(
      msg_log_section_start,
      indent=False,
      section=True,
  )
  controller.log(
      msg_log_filename_text_file.ljust(LOGGING_COLUMN1_WIDTH) +
      controller.settings.file_path,
      indent=False,
      section=False,
  )
  controller.log(
      msg_log_filename_schema.ljust(LOGGING_COLUMN1_WIDTH) +
      controller.settings.schema_path,
      indent=False,
      section=False,
  )
  yield None
  controller.log(
      msg_log_section_end,
      indent=False,
      section=True,
  )


@contextmanager
def assertion(
    controller: "Controller",
    operation: "AssertionBase",
) -> Generator[None, None, None]:
  start_index = controller.textfile.index
  yield None
  controller.log(
      operation,
      index=start_index,
  )


@contextmanager
def assertion_section(controller: "Controller") -> Generator[None, None, None]:
  controller.log(
      msg_log_section_assertions,
      indent=False,
      section=True,
  )
  yield None


@contextmanager
def validator(
    controller: "Controller",
    operation: "ValidationBase",
) -> Generator[None, None, None]:
  controller.log(operation)
  yield None


@contextmanager
def validator_section(controller: "Controller") -> Generator[None, None, None]:
  controller.log(
      msg_log_section_validators,
      indent=False,
      section=True,
  )
  yield None
