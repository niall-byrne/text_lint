"""Test the DeferredModuleLoaderBase class."""

from unittest import mock

from text_lint.cli.deferred.bases.deferred_base import DeferredModuleLoaderBase


class TestDeferredModuleLoaderBase:

  def test_initialize__attributes(
      self,
      concrete_deferred_module_loader_base_instance: DeferredModuleLoaderBase[
          mock.Mock],
      mocked_attribute: str,
      mocked_module_path: str,
  ) -> None:
    assert concrete_deferred_module_loader_base_instance.module_attribute == \
        mocked_attribute
    assert concrete_deferred_module_loader_base_instance.module_path == \
        mocked_module_path

  def test_call__calls_importlib(
      self,
      concrete_deferred_module_loader_base_instance: DeferredModuleLoaderBase[
          mock.Mock],
      mocked_importlib_module: mock.Mock,
  ) -> None:
    concrete_deferred_module_loader_base_instance()

    mocked_importlib_module.import_module.assert_called_once_with(
        concrete_deferred_module_loader_base_instance.module_path
    )

  def test_call__returns_correct_attribute(
      self,
      concrete_deferred_module_loader_base_instance: DeferredModuleLoaderBase[
          mock.Mock],
      mocked_importlib_module: mock.Mock,
  ) -> None:
    result = concrete_deferred_module_loader_base_instance()

    assert result == getattr(
        mocked_importlib_module.import_module.return_value,
        concrete_deferred_module_loader_base_instance.module_attribute,
    )
