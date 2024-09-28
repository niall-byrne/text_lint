"""Test the DeferredLinterSettings class."""

from text_lint.cli.deferred.bases.deferred_base import DeferredModuleLoaderBase
from ..deferred_linter_settings import DeferredLinterSettings


class TestDeferredLinterSettings:
  """Test the DeferredLinterSettings class."""

  def test_initialize__attributes(
      self,
      deferred_linter_settings_instance: DeferredLinterSettings,
  ) -> None:
    assert deferred_linter_settings_instance.module_attribute == \
        "LinterSettings"
    assert deferred_linter_settings_instance.module_path == \
        "text_lint.linter.settings"

  def test_initialize__inheritance(
      self,
      deferred_linter_settings_instance: DeferredLinterSettings,
  ) -> None:
    assert isinstance(
        deferred_linter_settings_instance,
        DeferredModuleLoaderBase,
    )
    assert isinstance(
        deferred_linter_settings_instance,
        DeferredLinterSettings,
    )
