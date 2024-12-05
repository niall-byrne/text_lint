"""Deferred import context manager."""

import importlib
from typing import Generic, TypeVar, cast

TypeDeferredModule = TypeVar("TypeDeferredModule")


class DeferredModuleLoaderBase(Generic[TypeDeferredModule]):
  """Deferred Python module loader."""

  module_attribute: str
  module_path: str

  def __call__(self) -> TypeDeferredModule:
    """Load the configured module, and return it.

    :returns: The module that has had loading deferred.
    """
    module = importlib.import_module(self.module_path)
    return cast(TypeDeferredModule, getattr(module, self.module_attribute))
