"""DeferredOperationDocumentation class."""

from typing import TYPE_CHECKING, Type

from .bases.deferred_base import DeferredModuleLoaderBase

if TYPE_CHECKING:  # no cover
  from text_lint.operations.documentation import \
      OperationDocumentation as OperationDocumentationType


class DeferredOperationDocumentation(
    DeferredModuleLoaderBase[Type["OperationDocumentationType"]]
):
  """Deferred OperationDocumentation loader."""

  module_path = "text_lint.operations.documentation"
  module_attribute = "OperationDocumentation"


deferred_operation_documentation = DeferredOperationDocumentation()
