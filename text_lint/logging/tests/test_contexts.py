"""Test the logging context module."""

from unittest import mock

from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOGGING_COLUMN1_WIDTH
from text_lint.logging import contexts as logging_contexts


class TestLoggingContexts:
  """Test the logging context managers."""

  def test_fmt_strings__are_translated(self) -> None:
    assert_is_translated(logging_contexts.msg_log_filename_text_file)
    assert_is_translated(logging_contexts.msg_log_filename_schema)
    assert_is_translated(logging_contexts.msg_log_section_assertions)
    assert_is_translated(logging_contexts.msg_log_section_end)
    assert_is_translated(logging_contexts.msg_log_section_start)
    assert_is_translated(logging_contexts.msg_log_section_validators)

  def test_main__calls_log_in_correct_sequence(
      self,
      mocked_controller: mock.Mock,
  ) -> None:
    mocked_controller.settings.file_path = "mocked/file/path"
    mocked_controller.settings.schema_path = "mocked/schema/path"

    with logging_contexts.main(mocked_controller):
      mocked_controller.log("inside context")

    assert mocked_controller.mock_calls == [
        mock.call.log(
            logging_contexts.msg_log_section_start,
            indent=False,
            section=True,
        ),
        mock.call.log(
            logging_contexts.msg_log_filename_text_file.
            ljust(LOGGING_COLUMN1_WIDTH) + mocked_controller.settings.file_path,
            indent=False,
            section=False,
        ),
        mock.call.log(
            logging_contexts.msg_log_filename_schema.
            ljust(LOGGING_COLUMN1_WIDTH) +
            mocked_controller.settings.schema_path,
            indent=False,
            section=False,
        ),
        mock.call.log("inside context"),
        mock.call.log(
            logging_contexts.msg_log_section_end,
            indent=False,
            section=True,
        ),
    ]

  def test_assertion__calls_log_in_correct_sequence(
      self,
      mocked_assertion: mock.Mock,
      mocked_controller: mock.Mock,
  ) -> None:
    mocked_controller.textfile.index = 10

    with logging_contexts.assertion(mocked_controller, mocked_assertion):
      mocked_controller.log("inside context")

    assert mocked_controller.mock_calls == [
        mock.call.log("inside context"),
        mock.call.log(
            mocked_assertion,
            index=mocked_controller.textfile.index,
        ),
    ]

  def test_assertion_sequence__calls_log_in_correct_sequence(
      self,
      mocked_controller: mock.Mock,
  ) -> None:
    with logging_contexts.assertion_section(mocked_controller):
      mocked_controller.log("inside context")

    assert mocked_controller.mock_calls == [
        mock.call.log(
            logging_contexts.msg_log_section_assertions,
            indent=False,
            section=True,
        ),
        mock.call.log("inside context"),
    ]

  def test_validator__calls_log_in_correct_sequence(
      self,
      mocked_validator: mock.Mock,
      mocked_controller: mock.Mock,
  ) -> None:
    with logging_contexts.validator(mocked_controller, mocked_validator):
      mocked_controller.log("inside context")

    assert mocked_controller.mock_calls == [
        mock.call.log(mocked_validator),
        mock.call.log("inside context"),
    ]

  def test_validator_sequence__calls_log_in_correct_sequence(
      self,
      mocked_controller: mock.Mock,
  ) -> None:
    with logging_contexts.validator_section(mocked_controller):
      mocked_controller.log("inside context")

    assert mocked_controller.mock_calls == [
        mock.call.log(
            logging_contexts.msg_log_section_validators,
            indent=False,
            section=True,
        ),
        mock.call.log("inside context"),
    ]
