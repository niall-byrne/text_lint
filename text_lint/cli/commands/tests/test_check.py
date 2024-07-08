"""Test the CheckCommand class."""

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
    assert check_command_instance.command_name == as_translation("check")
    assert check_command_instance.arg_filename_help == as_translation(
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
    assert_is_translated(check_command_instance.command_name)
    assert_is_translated(check_command_instance.arg_filename_help)
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
            "filenames",
            help=check_command_instance.arg_filename_help,
            type=file_type,
            nargs="+",
        ),
        mock.call(
            "-s",
            "--schema",
            help=check_command_instance.arg_schema_help,
            required=True,
            type=file_type,
        ),
    ]

  def test_invoke__starts_controller_correctly(
      self,
      mocked_controller: mock.Mock,
      check_command_instance: CheckCommand,
  ) -> None:
    mocked_args = mock.Mock()
    mocked_args.filenames = ["1.txt", "2.txt", "3.txt"]
    mocked_args.schema = "/path/to/schema.yml"

    check_command_instance.invoke(mocked_args)

    assert mocked_controller.call_count == 3
    assert mocked_controller.return_value.start.call_count == 3
    for index, mock_filename in enumerate(mocked_args.filenames):
      assert mocked_controller.mock_calls[index * 2:index * 2 + 2] == [
          mock.call(
              mock_filename,
              mocked_args.schema,
          ), mock.call().start()
      ]
