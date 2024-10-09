"""ThirdPartyExtensionsLoader class."""

import importlib.util
from types import ModuleType
from typing import List

from text_lint.utilities.translations import _
from .bases.loader_base import ExternalLoaderBase


class ThirdPartyExtensionsLoader(ExternalLoaderBase):
  """Load third-party supplied libraries of extensions."""

  msg_fmt_load_indicator = _(
      "<< {0} third-party extension(s) have been loaded! >>"
  )

  def __init__(self, modules: List[str]) -> None:
    super().__init__()
    self.modules = modules

  def load_modules(self) -> List[ModuleType]:
    """Generate a list of modules to import assertions from."""

    custom_modules: List[ModuleType] = []

    for target_file in self.modules:
      custom_modules.append(importlib.import_module(target_file))

    return custom_modules
