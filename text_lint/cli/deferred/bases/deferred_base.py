"""Deferred import context manager."""

import importlib
from typing import Generic, TypeVar, cast

TypeDeferredModule = TypeVar("TypeDeferredModule")


class DeferredModuleLoaderBase(Generic[TypeDeferredModule]):

  module_attribute: str
  module_path: str

  def __call__(self) -> TypeDeferredModule:
    module = importlib.import_module(self.module_path)
    return cast(TypeDeferredModule, getattr(module, self.module_attribute))
