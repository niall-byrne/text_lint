"""Test the text_lint command line interface."""

import argparse
from unittest import mock

import pytest
from text_lint.__helpers__.translations import (
    as_translation,
    assert_is_translated,
)
from text_lint.cli.commands.check_command import CheckCommand
from text_lint.cli.commands.documentation_command import DocumentationCommand
from text_lint.cli.commands.list_command import ListCommand
from .. import command_classes
from ..interface import TextLintCli
from .conftest import AliasArgumentMockCreator, AliasCommandMockCreator


class TestTextLintCli:
  """Test the text_lint command line interface."""

  def get_namespace(self, mocked_invoke: mock.Mock) -> argparse.Namespace:
    namespace = mocked_invoke.mock_calls[0].args[0]
    assert len(mocked_invoke.mock_calls[0].args) == 1
    assert len(mocked_invoke.mock_calls[0].kwargs) == 0
    assert isinstance(namespace, argparse.Namespace)
    return namespace

  def verify_mocked_command(
      self,
      cli_instance: TextLintCli,
      command_name: str,
  ) -> None:
    for command in cli_instance.command_instances:
      if command.command_name != command_name:
        assert not isinstance(command.invoke, mock.Mock)
      else:
        assert isinstance(command.invoke, mock.Mock)

  def test_initialize__attributes(
      self,
      cli_instance: TextLintCli,
  ) -> None:
    assert cli_instance.program_description == as_translation(
        "Generic text file linter."
    )
    assert cli_instance.program_command_help == as_translation("commands")
    assert cli_instance.program_name == as_translation("text_lint")

  def test_initialize__commands(
      self,
      cli_instance: TextLintCli,
  ) -> None:
    for index, command in enumerate(cli_instance.command_instances):
      assert isinstance(command, command_classes[index])

  def test_initialize__parser(
      self,
      cli_instance: TextLintCli,
  ) -> None:
    assert isinstance(cli_instance.parser, argparse.ArgumentParser)
    assert cli_instance.parser.prog == cli_instance.program_name
    assert cli_instance.parser.description == cli_instance.program_description

  def test_initialize__translations(
      self,
      cli_instance: TextLintCli,
  ) -> None:
    assert_is_translated(cli_instance.program_description)
    assert_is_translated(cli_instance.program_command_help)
    assert_is_translated(cli_instance.program_name)

  def test_invoke__no_arguments__displays_help(
      self,
      expected_help_string: str,
      create_mocked_arguments: AliasArgumentMockCreator,
      cli_instance: TextLintCli,
      capfd: pytest.CaptureFixture[str],
  ) -> None:
    create_mocked_arguments([])

    cli_instance.invoke()

    stdout, stderr = capfd.readouterr()
    assert stdout == expected_help_string
    assert stderr == ""

  def test_invoke__check_command__invokes_command_correctly(
      self,
      create_mocked_command: AliasCommandMockCreator,
      create_mocked_arguments: AliasArgumentMockCreator,
  ) -> None:
    mocked_files = ["file1", "file2", "file3"]
    create_mocked_arguments(
        [
            CheckCommand.command_name,
            "-s",
            "mocked_schema_file",
            "mock_file1",
            "mock_file2",
        ]
    )
    command_mocks = create_mocked_command(CheckCommand.command_name)
    self.verify_mocked_command(
        command_mocks.instance,
        CheckCommand.command_name,
    )
    command_mocks.file_type.side_effect = mocked_files

    command_mocks.instance.invoke()

    command_mocks.invoke.assert_called_once()

    namespace = self.get_namespace(command_mocks.invoke)
    assert namespace.command == CheckCommand.command_name
    assert namespace.schema == mocked_files[0]
    assert namespace.filenames == mocked_files[1:]

  def test_invoke__docs_command__invokes_command_correctly(
      self,
      create_mocked_command: AliasCommandMockCreator,
      create_mocked_arguments: AliasArgumentMockCreator,
  ) -> None:
    create_mocked_arguments(
        [
            DocumentationCommand.command_name,
            "assert_blank",
            "assert_equal",
        ]
    )
    command_mocks = create_mocked_command(DocumentationCommand.command_name)
    self.verify_mocked_command(
        command_mocks.instance,
        DocumentationCommand.command_name,
    )

    command_mocks.instance.invoke()

    command_mocks.invoke.assert_called_once()

    namespace = self.get_namespace(command_mocks.invoke)
    assert namespace.command == DocumentationCommand.command_name
    assert namespace.operations == ["assert_blank", "assert_equal"]

  def test_invoke__list_command__invokes_command_correctly(
      self,
      create_mocked_command: AliasCommandMockCreator,
      create_mocked_arguments: AliasArgumentMockCreator,
  ) -> None:
    create_mocked_arguments([ListCommand.command_name])
    command_mocks = create_mocked_command(ListCommand.command_name)
    self.verify_mocked_command(
        command_mocks.instance,
        ListCommand.command_name,
    )

    command_mocks.instance.invoke()

    command_mocks.invoke.assert_called_once()

    namespace = self.get_namespace(command_mocks.invoke)
    assert namespace.command == ListCommand.command_name
