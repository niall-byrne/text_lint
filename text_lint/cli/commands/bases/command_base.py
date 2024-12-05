"""CLICommandBase class."""

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from argparse import ArgumentParser, Namespace


class CLICommandBase(abc.ABC):
  """CLI command base class."""

  command_help: str
  command_name: str

  @abc.abstractmethod
  def create_parser(self, command_parser: "ArgumentParser") -> None:
    """Create an argument parser for this CLI command.

    :param command_parser: The root argparse parser to attach to.
    """

  @abc.abstractmethod
  def invoke(self, args: "Namespace") -> None:
    """Invoke this CLI command.

    :param args: The argparse namespace to use.
    """
