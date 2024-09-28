"""Test the DeferredOperationDocumentation class."""

from text_lint.cli.deferred.bases.deferred_base import DeferredModuleLoaderBase
from ..deferred_operation_documentation import DeferredOperationDocumentation


class TestDeferredOperationDocumentation:
  """Test the DeferredOperationDocumentation class."""

  def test_initialize__attributes(
      self,
      deferred_operation_documentation_instance: DeferredOperationDocumentation,
  ) -> None:
    assert deferred_operation_documentation_instance.module_attribute == \
        "OperationDocumentation"
    assert deferred_operation_documentation_instance.module_path == \
        "text_lint.operations.documentation"

  def test_initialize__inheritance(
      self,
      deferred_operation_documentation_instance: DeferredOperationDocumentation,
  ) -> None:
    assert isinstance(
        deferred_operation_documentation_instance,
        DeferredModuleLoaderBase,
    )
    assert isinstance(
        deferred_operation_documentation_instance,
        DeferredOperationDocumentation,
    )
