"""Test the CLICommandBase class."""

from text_lint.operations.documentation import OperationDocumentation
from ..command_base import CLICommandBase


class TestCLICommandBase:
  """Test the CLICommandBase class."""

  def test_initialize__attributes(
      self,
      mocked_command_help: str,
      mocked_command_name: str,
      concrete_cli_command_base_instance: CLICommandBase,
  ) -> None:
    assert concrete_cli_command_base_instance.command_help == (
        mocked_command_help
    )
    assert concrete_cli_command_base_instance.command_name == (
        mocked_command_name
    )
    assert isinstance(
        concrete_cli_command_base_instance.documentation,
        OperationDocumentation,
    )
