"""Test the CheckCommand class."""

from typing import List
from unittest import mock

from text_lint.__helpers__.translations import (
    as_translation,
    assert_is_translated,
)
from text_lint.cli.commands.bases.command_base import CLICommandBase
from text_lint.cli.types.file_type import file_type
from text_lint.operations.documentation import OperationDocumentation
from ..check_command import CheckCommand


class TestCheckCommand:
  """Test the CheckCommand class."""

  def test_initialize__attributes(
      self,
      check_command_instance: CheckCommand,
  ) -> None:
    assert check_command_instance.command_help == as_translation(
        "lint a text file"
    )
    assert check_command_instance.command_name == "check"
    assert check_command_instance.arg_filenames_help == as_translation(
        "the text file(s) to lint"
    )
    assert check_command_instance.arg_schema_help == as_translation(
        "the schema to apply"
    )
    assert isinstance(
        check_command_instance.documentation,
        OperationDocumentation,
    )

  def test_initialize__translations(
      self,
      check_command_instance: CheckCommand,
  ) -> None:
    assert_is_translated(check_command_instance.command_help)
    assert_is_translated(check_command_instance.arg_filenames)
    assert_is_translated(check_command_instance.arg_filenames_help)
    assert_is_translated(check_command_instance.arg_interpolate_schema_help)
    assert_is_translated(check_command_instance.arg_schema)
    assert_is_translated(check_command_instance.arg_schema_help)

  def test_initialize__inheritance(
      self,
      check_command_instance: CheckCommand,
  ) -> None:
    assert isinstance(
        check_command_instance,
        CLICommandBase,
    )
    assert isinstance(
        check_command_instance,
        CheckCommand,
    )

  def test_create_parser__adds_correct_arguments(
      self,
      check_command_instance: CheckCommand,
  ) -> None:
    mocked_command_parser = mock.Mock()

    check_command_instance.create_parser(mocked_command_parser)

    assert mocked_command_parser.add_argument.mock_calls == [
        mock.call(
            dest="filenames",
            help=check_command_instance.arg_filenames_help,
            metavar=check_command_instance.arg_filenames,
            nargs="+",
            type=file_type,
        ),
        mock.call(
            "-i",
            "--interpolate-schema",
            help=check_command_instance.arg_interpolate_schema_help,
            action='store_true'
        ),
        mock.call(
            "-s",
            "--schema",
            dest="schema",
            help=check_command_instance.arg_schema_help,
            metavar=check_command_instance.arg_schema,
            required=True,
            type=file_type,
        ),
    ]

  def test_invoke__configures_linter_correctly(
      self,
      mocked_args_check: mock.Mock,
      mocked_linter_settings: mock.Mock,
      check_command_instance: CheckCommand,
  ) -> None:

    check_command_instance.invoke(mocked_args_check)

    assert mocked_linter_settings.call_count == 3
    for index, mock_filename in enumerate(mocked_args_check.filenames):
      assert mocked_linter_settings.mock_calls[index] == mock.call(
          file_path=mock_filename,
          interpolate_schema=mocked_args_check.interpolate_schema,
          schema_path=mocked_args_check.schema,
      )

  def test_invoke__starts_linter_correctly(
      self,
      mocked_args_check: mock.Mock,
      mocked_linter: mock.Mock,
      mocked_linter_settings_instances: List[mock.Mock],
      check_command_instance: CheckCommand,
  ) -> None:
    check_command_instance.invoke(mocked_args_check)

    assert mocked_linter.call_count == 3
    assert mocked_linter.return_value.start.call_count == 3
    for index in range(len(mocked_args_check.filenames)):
      assert mocked_linter.mock_calls[index * 2:index * 2 + 2] == [
          mock.call(settings=mocked_linter_settings_instances[index]),
          mock.call().start(),
      ]
