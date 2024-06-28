"""Test the Logger class."""

from unittest import mock

import pytest
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import (
    LOGGING_COLUMN1_WIDTH,
    LOGGING_COLUMN2_WIDTH,
    LOGGING_INDENT,
)
from text_lint.linter.logging import Logger
from text_lint.utilities.whitespace import new_line


class TestLogger:
  """Test the Logger class."""

  def test_initialize__attributes(
      self,
      logger_instance: Logger,
      mocked_linter: mock.Mock,
  ) -> None:
    assert logger_instance.linter == mocked_linter

  def test_initialize__translations(
      self,
      logger_instance: Logger,
  ) -> None:
    assert_is_translated(logger_instance.msg_fmt_log_validator_prefix)
    assert_is_translated(logger_instance.msf_fmt_log_unsupported_object)

  def test_call__string__defaults__correct_stdout(
      self,
      logger_instance: Logger,
      capfd: pytest.CaptureFixture[str],
  ) -> None:
    mocked_message = "mocked_message"

    logger_instance(mocked_message)

    stdout, stderr = capfd.readouterr()
    assert stdout == new_line(mocked_message)
    assert stderr == ""

  @pytest.mark.parametrize(
      "indent,section,fmt_string",
      [
          (True, True, LOGGING_INDENT + Logger.msg_fmt_log_section),
          (True, False, LOGGING_INDENT + "{0}"),
          (False, True, Logger.msg_fmt_log_section),
          (False, False, "{0}"),
      ],
  )
  def test_call__string__vary_index__vary_indent__correct_stdout(
      self,
      logger_instance: Logger,
      capfd: pytest.CaptureFixture[str],
      indent: bool,
      section: bool,
      fmt_string: str,
  ) -> None:
    mocked_message = "mocked_message"

    logger_instance(mocked_message, indent=indent, section=section)

    stdout, stderr = capfd.readouterr()
    assert stdout == new_line(fmt_string.format(mocked_message))
    assert stderr == ""

  def test_call__assertion__current_index__correct_stdout(
      self,
      logger_instance: Logger,
      mocked_assertion: mock.Mock,
      mocked_linter: mock.Mock,
      capfd: pytest.CaptureFixture[str],
  ) -> None:
    text_file_start_index = 10
    mocked_linter.textfile.index = text_file_start_index

    logger_instance(mocked_assertion, index=text_file_start_index)

    stdout, stderr = capfd.readouterr()
    assert stdout == new_line(
        "{0}".format(text_file_start_index + 1).ljust(LOGGING_COLUMN1_WIDTH) +
        mocked_assertion.operation.ljust(LOGGING_COLUMN2_WIDTH) +
        mocked_assertion.name
    )
    assert stderr == ""

  def test_call__assertion__ranged_index__correct_stdout(
      self,
      logger_instance: Logger,
      mocked_assertion: mock.Mock,
      mocked_linter: mock.Mock,
      capfd: pytest.CaptureFixture[str],
  ) -> None:
    text_file_start_index = 5
    mocked_linter.textfile.index = text_file_start_index + 5

    logger_instance(mocked_assertion, index=text_file_start_index)

    stdout, stderr = capfd.readouterr()
    assert stdout == new_line(
        "{0}-{1}".format(
            text_file_start_index + 1,
            text_file_start_index + 1 + 5,
        ).ljust(LOGGING_COLUMN1_WIDTH) +
        mocked_assertion.operation.ljust(LOGGING_COLUMN2_WIDTH) +
        mocked_assertion.name
    )
    assert stderr == ""

  def test_call__validator__correct_stdout(
      self,
      logger_instance: Logger,
      mocked_linter: mock.Mock,
      mocked_validator: mock.Mock,
      capfd: pytest.CaptureFixture[str],
  ) -> None:
    text_file_start_index = 10
    mocked_linter.textfile.index = text_file_start_index

    logger_instance(mocked_validator)

    stdout, stderr = capfd.readouterr()
    assert stdout == new_line(
        Logger.msg_fmt_log_validator_prefix.ljust(LOGGING_COLUMN1_WIDTH) +
        mocked_validator.operation.ljust(LOGGING_COLUMN2_WIDTH) +
        mocked_validator.name
    )
    assert stderr == ""

  def test_call__unsupported_object__correct_stdout(
      self,
      logger_instance: Logger,
      capfd: pytest.CaptureFixture[str],
  ) -> None:
    unsupported_object = mock.Mock()

    logger_instance(unsupported_object)

    stdout, stderr = capfd.readouterr()
    assert stdout == new_line(
        Logger.msf_fmt_log_unsupported_object.format(unsupported_object)
    )
    assert stderr == ""
