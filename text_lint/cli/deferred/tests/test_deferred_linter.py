"""Test the DeferredLinter class."""

from text_lint.cli.deferred.bases.deferred_base import DeferredModuleLoaderBase
from ..deferred_linter import DeferredLinter


class TestDeferredLinter:
  """Test the DeferredLinter class."""

  def test_initialize__attributes(
      self,
      deferred_linter_instance: DeferredLinter,
  ) -> None:
    assert deferred_linter_instance.module_attribute == \
        "Linter"
    assert deferred_linter_instance.module_path == \
        "text_lint.linter"

  def test_initialize__inheritance(
      self,
      deferred_linter_instance: DeferredLinter,
  ) -> None:
    assert isinstance(
        deferred_linter_instance,
        DeferredModuleLoaderBase,
    )
    assert isinstance(
        deferred_linter_instance,
        DeferredLinter,
    )
