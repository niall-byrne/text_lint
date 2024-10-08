"""CLI Command Base Class"""

import abc
from typing import TYPE_CHECKING

from text_lint.operations.documentation import OperationDocumentation

if TYPE_CHECKING:  # pragma: no cover
  from argparse import ArgumentParser, Namespace


class CLICommandBase(abc.ABC):
  """CLI Command Base Command."""

  command_help: str
  command_name: str

  def __init__(self) -> None:
    self.documentation = OperationDocumentation()

  @abc.abstractmethod
  def create_parser(self, command_parser: "ArgumentParser") -> None:
    """Create an argument parser for this CLI command."""

  @abc.abstractmethod
  def invoke(self, args: "Namespace") -> None:
    """Invoke this CLI command."""
