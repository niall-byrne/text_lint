"""CheckCommand class."""

from argparse import ArgumentParser, Namespace

from text_lint.cli.commands.bases.command_base import CLICommandBase
from text_lint.cli.types.file_type import file_type
from text_lint.controller import Controller
from text_lint.utilities.translations import _


class CheckCommand(CLICommandBase):
  """CLI command to lint a specific file with a specific schema."""

  command_help = _("lint a text file")
  command_name = _("check")

  arg_filename_help = _("the text file(s) to lint")
  arg_schema_help = _("the schema to apply")

  def create_parser(self, command_parser: "ArgumentParser") -> None:
    """Create an argument parser for this CLI command."""

    command_parser.add_argument(
        "filenames",
        help=self.arg_filename_help,
        type=file_type,
        nargs="+",
    )
    command_parser.add_argument(
        "-s",
        "--schema",
        help=self.arg_schema_help,
        required=True,
        type=file_type,
    )

  def invoke(self, args: "Namespace") -> None:
    """Invoke this CLI command."""

    for filename in args.filenames:
      ctrl = Controller(filename, args.schema)
      ctrl.start()
