"""The text_lint CLI."""

from typing import Sequence, Type

from text_lint.cli.commands.bases.command_base import CLICommandBase
from text_lint.cli.commands.check_command import CheckCommand
from text_lint.cli.commands.documentation_command import DocumentationCommand
from text_lint.cli.commands.list_command import ListCommand

command_classes: Sequence[Type[CLICommandBase]] = [
    CheckCommand,
    DocumentationCommand,
    ListCommand,
]
