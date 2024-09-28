"""ListCommand class."""

from argparse import ArgumentParser, Namespace

from text_lint.cli.commands.bases.command_base import CLICommandBase
from text_lint.cli.deferred.deferred_operation_documentation import (
    deferred_operation_documentation,
)
from text_lint.utilities.translations import _


class ListCommand(CLICommandBase):
  """CLI command to list the available operations."""

  command_help = _("list all available operations")
  command_name = "list"

  def create_parser(self, command_parser: "ArgumentParser") -> None:
    """Create an argument parser for this CLI command."""

  def invoke(self, args: "Namespace") -> None:
    """Invoke this CLI command."""

    documentation = deferred_operation_documentation()()
    documentation.list()
    documentation.print()
