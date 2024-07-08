"""The text_lint command line interface."""

import argparse

from text_lint.utilities.translations import _
from . import command_classes


class TextLintCli:
  """The text_lint CLI."""

  program_name = "text_lint"
  program_description = _("Generic text file linter.")

  arg_command = _("command")
  arg_command_help = _("description")
  arg_help_help = _("show this help message and exit")

  def __init__(self) -> None:
    self.command_instances = [command() for command in command_classes]
    self.parser = argparse.ArgumentParser(
        description=self.program_description,
        prog=self.program_name,
        add_help=False,
    )
    self.parser.add_argument(
        "-h",
        "--help",
        dest="help",
        help=self.arg_help_help,
        action="store_true",
    )
    subparsers = self.parser.add_subparsers(
        help=self.arg_command_help,
        metavar=self.arg_command,
        dest="command",
    )
    for command in self.command_instances:
      command_parser = subparsers.add_parser(
          command.command_name,
          help=command.command_help,
      )
      command.create_parser(command_parser)

  def invoke(self) -> None:
    args = self.parser.parse_args()
    for command in self.command_instances:
      if args.command == command.command_name:
        command.invoke(args)
        break
    else:
      self.parser.print_help()
