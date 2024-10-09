"""Test the ThirdPartyExtensionsLoader class."""

from typing import List
from unittest import mock

from ..bases.loader_base import ExternalLoaderBase
from ..third_party import ThirdPartyExtensionsLoader


class TestThirdPartyExtensionsLoader:
  """Test the ThirdPartyExtensionsLoader class."""

  def test_initialize__attributes(
      self,
      mocked_module_names: List[str],
      third_party_extensions_loader_instance: ThirdPartyExtensionsLoader,
  ) -> None:
    assert third_party_extensions_loader_instance.modules == (
        mocked_module_names
    )

  def test_initialize__inheritance(
      self,
      third_party_extensions_loader_instance: ThirdPartyExtensionsLoader,
  ) -> None:
    assert isinstance(
        third_party_extensions_loader_instance,
        ThirdPartyExtensionsLoader,
    )
    assert isinstance(
        third_party_extensions_loader_instance,
        ExternalLoaderBase,
    )

  def test_load_modules__returns_modules(
      self,
      mocked_importlib: mock.Mock,
      mocked_module_names: List[str],
      third_party_extensions_loader_instance: ThirdPartyExtensionsLoader,
  ) -> None:
    mocked_importlib.import_module.side_effect = (
        lambda module_name: mock.Mock(**{"module_name": module_name})
    )

    modules = third_party_extensions_loader_instance.load_modules()

    for module, mocked_module_name in zip(modules, mocked_module_names):
      assert module.module_name == mocked_module_name
    assert len(modules) == len(mocked_module_names)

  def test_load_modules__call_importlib(
      self,
      mocked_importlib: mock.Mock,
      mocked_module_names: List[str],
      third_party_extensions_loader_instance: ThirdPartyExtensionsLoader,
  ) -> None:
    third_party_extensions_loader_instance.load_modules()

    assert mocked_importlib.import_module.mock_calls == list(
        map(
            mock.call,
            mocked_module_names,
        )
    )
