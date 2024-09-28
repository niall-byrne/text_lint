"""DeferredLinter class."""

from typing import TYPE_CHECKING, Type

from .bases.deferred_base import DeferredModuleLoaderBase

if TYPE_CHECKING:  # no cover
  from text_lint.linter import Linter as LinterType


class DeferredLinter(DeferredModuleLoaderBase[Type["LinterType"]]):
  """Deferred Linter loader."""

  module_path = "text_lint.linter"
  module_attribute = "Linter"


deferred_linter = DeferredLinter()
