"""LocalFolderExtensionsLoader class."""

import importlib.util
import os
from types import ModuleType
from typing import List

from text_lint.exceptions.external import ExternalLoaderFailedImport
from text_lint.utilities.translations import _
from .bases.loader_base import ExternalLoaderBase


class LocalFolderExtensionsLoader(ExternalLoaderBase):
  """Load local folder supplied libraries of extensions."""

  msg_fmt_load_indicator = _(
      "<< {0} local extension(s) have been loaded! >>"
  )

  def __init__(self, paths: List[str]) -> None:
    super().__init__()
    self.local_paths = paths

  def load_modules(self) -> List[ModuleType]:
    """Generate a list of modules to import assertions from."""

    custom_modules: List[ModuleType] = []

    for target_file in self._get_local_python_sources():
      custom_modules.append(self._load_local_modules(target_file))

    return custom_modules

  def _get_local_python_sources(self) -> List[str]:
    return [
        entry.path
        for path in self.local_paths
        for entry in os.scandir(path)
        if entry.is_file() and entry.path.endswith(".py")
    ]

  def _load_local_modules(self, target_file: str) -> ModuleType:
    try:
      spec = importlib.util.spec_from_file_location(
          os.path.dirname(target_file),
          target_file,
      )
      assert spec is not None
      assert spec.loader is not None
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)
      return module
    except AssertionError as exc:
      raise ExternalLoaderFailedImport(target_file) from exc
