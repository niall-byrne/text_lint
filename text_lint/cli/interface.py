"""The text_lint command line interface."""

import argparse
import os
from typing import List

from text_lint import env_vars
from text_lint.cli.types.directory_type import directory_type
from text_lint.operations.external.local import LocalFolderExtensionsLoader
from text_lint.operations.external.third_party import (
    ThirdPartyExtensionsLoader,
)
from text_lint.utilities.translations import _
from . import command_classes


class TextLintCli:
  """The text_lint CLI."""

  program_name = "text_lint"
  program_description = _("Generic text file linter.")

  arg_command = _("command")
  arg_command_help = _("description")
  arg_help_help = _("show this help message and exit")
  arg_local_folder = _("folder_name")
  arg_local_folder_help = _(
      "local folder containing custom extensions"
  )
  arg_third_party = _("package_name")
  arg_third_party_help = _(
      "python package containing custom extensions"
  )

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
    self.parser.add_argument(
        "-l",
        "--local-folder",
        action='append',
        default=self._default_from_env_var(
            env_var_name=env_vars.EXTENSIONS_LOCAL_ENV_VAR,
            seperator=env_vars.EXTENSIONS_LOCAL_VAR_SEPERATOR
        ),
        dest="local_folder",
        help=self.arg_local_folder_help,
        metavar=self.arg_local_folder,
        type=directory_type,
    )
    self.parser.add_argument(
        "-t",
        "--third-party",
        action='append',
        default=self._default_from_env_var(
            env_var_name=env_vars.EXTENSIONS_THIRD_PARTY_ENV_VAR,
            seperator=env_vars.EXTENSIONS_THIRD_PARTY_VAR_SEPERATOR,
        ),
        dest="third_party",
        help=self.arg_third_party_help,
        metavar=self.arg_third_party,
        type=str,
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

  def _default_from_env_var(
      self,
      env_var_name: str,
      seperator: str,
  ) -> List[str]:
    env_var = os.getenv(env_var_name)
    if env_var:
      return env_var.split(seperator)
    return []

  def invoke(self) -> None:
    args = self.parser.parse_args()

    self._load_extensions(args)

    for command in self.command_instances:
      if args.command == command.command_name:
        command.invoke(args)
        break
    else:
      self.parser.print_help()

  def _load_extensions(self, args: argparse.Namespace) -> None:
    LocalFolderExtensionsLoader(args.local_folder).load()
    ThirdPartyExtensionsLoader(args.third_party).load()
