"""Test the DocumentationCommand class."""

from unittest import mock

from text_lint.__helpers__.translations import (
    as_translation,
    assert_is_translated,
)
from text_lint.cli.commands.bases.command_base import CLICommandBase
from ..documentation_command import DocumentationCommand


class TestDocumentationCommand:
  """Test the DocumentationCommand class."""

  def test_initialize__attributes(
      self,
      mocked_documentation: mock.Mock,
      documentation_command_instance: DocumentationCommand,
  ) -> None:
    assert documentation_command_instance.command_help == as_translation(
        "document the available operations"
    )
    assert documentation_command_instance.command_name == "doc"
    assert documentation_command_instance.arg_operations_help == as_translation(
        "the operation(s) to document"
    )
    assert documentation_command_instance.documentation == mocked_documentation

  def test_initialize__translations(
      self,
      documentation_command_instance: DocumentationCommand,
  ) -> None:
    assert_is_translated(documentation_command_instance.command_help)
    assert_is_translated(documentation_command_instance.arg_operations)
    assert_is_translated(documentation_command_instance.arg_operations_help)

  def test_initialize__inheritance(
      self,
      documentation_command_instance: DocumentationCommand,
  ) -> None:
    assert isinstance(
        documentation_command_instance,
        CLICommandBase,
    )
    assert isinstance(
        documentation_command_instance,
        DocumentationCommand,
    )

  def test_create_parser__adds_correct_arguments(
      self,
      documentation_command_instance: DocumentationCommand,
  ) -> None:
    mocked_command_parser = mock.Mock()

    documentation_command_instance.create_parser(mocked_command_parser)

    assert mocked_command_parser.add_argument.mock_calls == [
        mock.call(
            dest="operations",
            help=documentation_command_instance.arg_operations_help,
            metavar=documentation_command_instance.arg_operations,
            nargs="+",
            type=str,
        ),
    ]

  def test_invoke__lists_and_prints_documentation(
      self,
      mocked_args_documentation: mock.Mock,
      mocked_documentation: mock.Mock,
      documentation_command_instance: DocumentationCommand,
  ) -> None:
    documentation_command_instance.invoke(mocked_args_documentation)

    assert mocked_documentation.search.call_count == 3
    assert mocked_documentation.print.call_count == 1
    assert mocked_documentation.mock_calls == [
        mock.call.search(mocked_operation)
        for mocked_operation in mocked_args_documentation.operations
    ] + [mock.call.print()]
