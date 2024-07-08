"""Test the ListCommand class."""

from unittest import mock

from text_lint.__helpers__.translations import (
    as_translation,
    assert_is_translated,
)
from text_lint.cli.commands.bases.command_base import CLICommandBase
from ..list_command import ListCommand


class TestListCommand:
  """Test the ListCommand class."""

  def test_initialize__attributes(
      self,
      mocked_documentation: mock.Mock,
      list_command_instance: ListCommand,
  ) -> None:
    assert list_command_instance.command_help == as_translation(
        "list all available operations"
    )
    assert list_command_instance.command_name == "list"
    assert list_command_instance.documentation == mocked_documentation

  def test_initialize__translations(
      self,
      list_command_instance: ListCommand,
  ) -> None:
    assert_is_translated(list_command_instance.command_help)

  def test_initialize__inheritance(
      self,
      list_command_instance: ListCommand,
  ) -> None:
    assert isinstance(
        list_command_instance,
        CLICommandBase,
    )
    assert isinstance(
        list_command_instance,
        ListCommand,
    )

  def test_create_parser__is_a_noop(
      self,
      list_command_instance: ListCommand,
  ) -> None:
    mocked_command_parser = mock.Mock()

    list_command_instance.create_parser(mocked_command_parser)

  def test_invoke__lists_and_prints_documentation(
      self,
      mocked_args_list: mock.Mock,
      mocked_documentation: mock.Mock,
      list_command_instance: ListCommand,
  ) -> None:
    list_command_instance.invoke(mocked_args_list)

    assert mocked_documentation.mock_calls == [
        mock.call.list(),
        mock.call.print(),
    ]
