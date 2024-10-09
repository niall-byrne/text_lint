"""Shared test fixtures for the text_lint CLI interface."""
# pylint: disable=redefined-outer-name

import sys
from typing import Callable, List, NamedTuple
from unittest import mock

import pytest
from text_lint.config import NEW_LINE
from .. import command_classes, interface

HELP_FORMAT_STRING = """usage: {0} [-h] [-l {1}] [-t {2}]
                 {3} ...

{program_description}

positional arguments:
  {command}     {description}
"""
HELP_SUFFIX = """
optional arguments:
  -h, --help            {help}
  -l {0}, --local-folder {0}
                        {local_folder}
  -t {1}, --third-party {1}
                        {third_party}
"""
HELP_COMMAND_SPACING = 20

AliasArgumentMockCreator = Callable[[List[str]], None]
AliasPatchedCliCreator = Callable[[str], "CLIMocks"]


class CLIMocks(NamedTuple):
  file_type: mock.Mock
  invoke: mock.Mock
  instance: interface.TextLintCli
  local_extension_loader: mock.Mock
  third_party_extension_loader: mock.Mock


@pytest.fixture
def mocked_argument_parser(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(
      interface.argparse,
      "ArgumentParser",
      instance,
  )
  return instance


@pytest.fixture
def create_mocked_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> AliasArgumentMockCreator:

  def setup(arguments: List[str]) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [interface.TextLintCli.program_name] + arguments,
    )

  return setup


@pytest.fixture
def create_patched_cli_instance(
    monkeypatch: pytest.MonkeyPatch,
) -> AliasPatchedCliCreator:

  def setup(command_name: str) -> CLIMocks:
    command_class = next(
        filter(
            lambda command: command.command_name == command_name,
            command_classes,
        )
    )

    mocked_invoke = mock.Mock()
    mocked_file_type = mock.Mock()
    mocked_local_extension_loader = mock.Mock()
    mocked_third_party_extension_loader = mock.Mock()

    monkeypatch.setattr(
        interface,
        "LocalFolderExtensionsLoader",
        mocked_local_extension_loader,
    )
    monkeypatch.setattr(
        interface,
        "ThirdPartyExtensionsLoader",
        mocked_third_party_extension_loader,
    )

    monkeypatch.setattr(command_class, "invoke", mocked_invoke)

    try:
      monkeypatch.setattr(
          command_class.__module__ + ".file_type",
          mocked_file_type,
      )
    except AttributeError:
      pass

    return CLIMocks(
        file_type=mocked_file_type,
        invoke=mocked_invoke,
        instance=interface.TextLintCli(),
        local_extension_loader=mocked_local_extension_loader,
        third_party_extension_loader=mocked_third_party_extension_loader,
    )

  return setup


@pytest.fixture
def expected_help_string() -> str:
  help_string = HELP_FORMAT_STRING.format(
      interface.TextLintCli.program_name,
      interface.TextLintCli.arg_local_folder,
      interface.TextLintCli.arg_third_party,
      interface.TextLintCli.arg_command,
      command=interface.TextLintCli.arg_command,
      description=interface.TextLintCli.arg_command_help,
      program_description=interface.TextLintCli.program_description,
  )

  for command in command_classes:
    help_string += "".join(
        [
            "    ",
            command.command_name.ljust(HELP_COMMAND_SPACING),
            command.command_help,
            NEW_LINE,
        ]
    )

  help_string += HELP_SUFFIX.format(
      interface.TextLintCli.arg_local_folder,
      interface.TextLintCli.arg_third_party,
      help=interface.TextLintCli.arg_help_help,
      local_folder=interface.TextLintCli.arg_local_folder_help,
      third_party=interface.TextLintCli.arg_third_party_help,
  )

  return help_string


@pytest.fixture
def cli_instance() -> interface.TextLintCli:
  return interface.TextLintCli()
