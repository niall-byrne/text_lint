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
    assert documentation_command_instance.command_name == as_translation("doc")
    assert documentation_command_instance.arg_operation_help == as_translation(
        "the operation(s) to document"
    )
    assert documentation_command_instance.documentation == mocked_documentation

  def test_initialize__translations(
      self,
      documentation_command_instance: DocumentationCommand,
  ) -> None:
    assert_is_translated(documentation_command_instance.command_help)
    assert_is_translated(documentation_command_instance.command_name)
    assert_is_translated(documentation_command_instance.arg_operation_help)

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
            "operations",
            help=documentation_command_instance.arg_operation_help,
            type=str,
            nargs="+",
        ),
    ]

  def test_invoke__lists_and_prints_documentation(
      self,
      mocked_documentation: mock.Mock,
      documentation_command_instance: DocumentationCommand,
  ) -> None:
    mocked_args = mock.Mock()
    mocked_args.operations = ["operation1", "operation2", "operation3"]

    documentation_command_instance.invoke(mocked_args)

    assert mocked_documentation.search.call_count == 3
    assert mocked_documentation.print.call_count == 3
    for index, mocked_operation in enumerate(mocked_args.operations):
      assert mocked_documentation.mock_calls[index * 2:index * 2 + 2] == [
          mock.call.search(mocked_operation),
          mock.call.print()
      ]
