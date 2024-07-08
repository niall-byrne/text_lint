"""DocumentationCommand class."""

from argparse import ArgumentParser, Namespace

from text_lint.cli.commands.bases.command_base import CLICommandBase
from text_lint.utilities.translations import _


class DocumentationCommand(CLICommandBase):
  """CLI command to document the available operations."""

  command_help = _("document the available operations")
  command_name = _("doc")

  arg_operation_help = _("the operation(s) to document")

  def create_parser(self, command_parser: "ArgumentParser") -> None:
    """Create an argument parser for this CLI command."""

    command_parser.add_argument(
        "operations",
        help=self.arg_operation_help,
        type=str,
        nargs="+",
    )

  def invoke(self, args: "Namespace") -> None:
    """Invoke this CLI command."""

    for operation in args.operations:
      self.documentation.search(operation)
      self.documentation.print()
