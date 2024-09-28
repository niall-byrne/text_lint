"""DocumentationCommand class."""

from argparse import ArgumentParser, Namespace

from text_lint.cli.commands.bases.command_base import CLICommandBase
from text_lint.cli.deferred.deferred_operation_documentation import (
    deferred_operation_documentation,
)
from text_lint.utilities.translations import _


class DocumentationCommand(CLICommandBase):
  """CLI command to document the available operations."""

  command_help = _("document the available operations")
  command_name = "doc"

  arg_operations = _("operations")
  arg_operations_help = _("the operation(s) to document")

  def create_parser(self, command_parser: "ArgumentParser") -> None:
    """Create an argument parser for this CLI command."""

    command_parser.add_argument(
        dest="operations",
        help=self.arg_operations_help,
        metavar=self.arg_operations,
        nargs="+",
        type=str,
    )

  def invoke(self, args: "Namespace") -> None:
    """Invoke this CLI command."""

    documentation = deferred_operation_documentation()()

    for operation in args.operations:
      documentation.search(operation)

    documentation.print()
