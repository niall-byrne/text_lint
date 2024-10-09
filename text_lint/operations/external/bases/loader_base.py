"""ExternalLoaderBase class."""
import abc
import sys
from types import ModuleType
from typing import Any, Dict, Sequence, Tuple, Type, Union

from text_lint.operations.assertions import assertion_registry
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.lookups import lookup_registry
from text_lint.operations.lookups.bases.lookup_base import LookupBase
from text_lint.operations.validators import validator_registry
from text_lint.operations.validators.bases.validator_base import ValidatorBase
from text_lint.operations.validators.expressions import expressions_registry
from text_lint.operations.validators.expressions.bases.expression_base import (
    ExpressionBase,
)
from text_lint.utilities.translations import f

AliasExtensionBaseClass = Type[Union[
    AssertionBase,
    ExpressionBase,
    LookupBase,
    ValidatorBase,
]]
AliasRegistry = Dict[str, Any]
AliasRegistryMappings = Sequence[
    Tuple[
        AliasExtensionBaseClass,
        AliasRegistry,
        str,
    ],
]


class ExternalLoaderBase(abc.ABC):
  """Base class for loading extensions."""

  mappings_registry: AliasRegistryMappings

  msg_fmt_load_indicator: str

  def __init__(self) -> None:
    self.loaded_extensions = 0
    self.mappings_registry = (
        (AssertionBase, assertion_registry, "operation"),
        (ExpressionBase, expressions_registry, "operator"),
        (LookupBase, lookup_registry, "operation"),
        (ValidatorBase, validator_registry, "operation"),
    )

  def load(self) -> None:
    """Load extensions from a list of loaded python modules."""

    for module in self.load_modules():
      for available_import_name in dir(module):
        available_import = getattr(module, available_import_name)
        self._import_to_registry(available_import)

    self._display_indicator()

  @abc.abstractmethod
  def load_modules(self) -> Sequence[ModuleType]:
    """Generate an iterable of modules to import extensions from."""

  def _import_to_registry(
      self,
      available_import: Any,
  ) -> None:
    if isinstance(available_import, type):
      for base_class, registry, attribute_name in self.mappings_registry:
        if issubclass(
            available_import,
            base_class,
        ) and available_import != base_class:
          registry_key: str = getattr(available_import, attribute_name)
          registry[registry_key] = available_import
          self.loaded_extensions += 1

  def _display_indicator(self) -> None:
    if self.loaded_extensions:
      sys.stdout.write(
          f(
              self.msg_fmt_load_indicator,
              self.loaded_extensions,
              nl=2,
          )
      )
