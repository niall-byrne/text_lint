"""The text_lint command line interface."""

import argparse

from text_lint.utilities.translations import _
from . import command_classes


class TextLintCli:
  """The text_lint CLI."""

  program_description = _("Generic text file linter.")
  program_command_help = _("commands")
  program_name = _("text_lint")

  def __init__(self) -> None:
    self.command_instances = [command() for command in command_classes]
    self.parser = argparse.ArgumentParser(
        prog=self.program_name,
        description=self.program_description,
    )
    subparsers = self.parser.add_subparsers(
        help=self.program_command_help,
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
