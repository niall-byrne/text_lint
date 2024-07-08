"""Shared test fixtures for the text_lint CLI command bases."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, Type

import pytest
from ..command_base import CLICommandBase

if TYPE_CHECKING:  # pragma: no cover
  from argparse import ArgumentParser, Namespace


@pytest.fixture
def mocked_command_help() -> str:
  return "mocked_command_help"


@pytest.fixture
def mocked_command_name() -> str:
  return "mocked_command_name"


@pytest.fixture
def concrete_cli_command_base_class(
    mocked_command_help: str,
    mocked_command_name: str,
) -> Type[CLICommandBase]:

  class ConcreteCLICommand(CLICommandBase):

    command_help = mocked_command_help
    command_name = mocked_command_name

    def create_parser(self, command_parser: "ArgumentParser") -> None:
      """Create an argument parser for this CLI command."""

    def invoke(self, args: "Namespace") -> None:
      """Invoke this CLI command."""

  return ConcreteCLICommand


@pytest.fixture
def concrete_cli_command_base_instance(
    concrete_cli_command_base_class: Type[CLICommandBase]
) -> CLICommandBase:
  return concrete_cli_command_base_class()
