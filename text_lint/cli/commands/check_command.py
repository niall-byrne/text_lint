"""CheckCommand class."""

from argparse import ArgumentParser, Namespace

from text_lint.cli.commands.bases.command_base import CLICommandBase
from text_lint.cli.deferred.deferred_linter import deferred_linter
from text_lint.cli.deferred.deferred_linter_settings import (
    deferred_linter_settings,
)
from text_lint.cli.types.file_type import file_type
from text_lint.utilities.translations import _


class CheckCommand(CLICommandBase):
  """CLI command to lint a specific file with a specific schema."""

  command_help = _("lint a text file")
  command_name = "check"

  arg_filenames = _("filenames")
  arg_filenames_help = _("the text file(s) to lint")
  arg_interpolate_schema_help = _(
      "use environment variables to interpolate the schema file"
  )
  arg_quiet_help = _("suppress non critical messages")
  arg_schema = _("schema")
  arg_schema_help = _("the schema to apply")

  def create_parser(self, command_parser: "ArgumentParser") -> None:
    """Create an argument parser for this CLI command."""

    command_parser.add_argument(
        dest="filenames",
        help=self.arg_filenames_help,
        metavar=self.arg_filenames,
        nargs="+",
        type=file_type,
    )
    command_parser.add_argument(
        "-i",
        "--interpolate-schema",
        help=self.arg_interpolate_schema_help,
        action='store_true'
    )
    command_parser.add_argument(
        "-q",
        "--quiet",
        help=self.arg_quiet_help,
        action='store_true',
    )
    command_parser.add_argument(
        "-s",
        "--schema",
        dest="schema",
        help=self.arg_schema_help,
        metavar=self.arg_schema,
        required=True,
        type=file_type,
    )

  def invoke(self, args: "Namespace") -> None:
    """Invoke this CLI command."""

    for filename in args.filenames:
      settings = deferred_linter_settings()(
          file_path=filename,
          interpolate_schema=args.interpolate_schema,
          quiet=args.quiet,
          schema_path=args.schema
      )
      linter = deferred_linter()(settings=settings)
      linter.start()
