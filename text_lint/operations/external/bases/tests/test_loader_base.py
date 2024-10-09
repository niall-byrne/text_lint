"""Test the ExternalLoaderBase class."""

import pytest
from text_lint.utilities.translations import f
from ..loader_base import ExternalLoaderBase
from .conftest import AliasMockedRegistries, all_mocked_extensions


class TestExternalLoaderBase:
  """Test the ExternalLoaderBase class."""

  def test_initialize__attributes(
      self,
      concrete_external_loader_base_instance: ExternalLoaderBase,
      mocked_registries: AliasMockedRegistries,
  ) -> None:
    assert concrete_external_loader_base_instance.loaded_extensions == 0
    for base_class, registry, _ in (
        concrete_external_loader_base_instance.mappings_registry
    ):
      assert mocked_registries[base_class] == registry

  @pytest.mark.parametrize("extension_fixture", all_mocked_extensions)
  def test_load__vary_module_contents__one_extension__updates_one_registry(
      self,
      concrete_external_loader_base_instance: ExternalLoaderBase,
      extension_fixture: str,
      request: pytest.FixtureRequest,
  ) -> None:
    selected_extension, selected_base_class = request.getfixturevalue(
        extension_fixture
    )

    concrete_external_loader_base_instance.load()

    for base_class, registry, attribute_name in (
        concrete_external_loader_base_instance.mappings_registry
    ):
      if base_class == selected_base_class:
        registry_key = getattr(selected_extension, attribute_name)
        assert registry[registry_key] == selected_extension
      else:
        assert len(registry) == 0

  def test_load__vary_module_contents__one_of_each_extension__updates_registry(
      self,
      concrete_external_loader_base_instance: ExternalLoaderBase,
      request: pytest.FixtureRequest,
  ) -> None:
    created_extensions = [
        request.getfixturevalue(extension_fixture)
        for extension_fixture in all_mocked_extensions
    ]

    concrete_external_loader_base_instance.load()

    for base_class, registry, attribute_name in (
        concrete_external_loader_base_instance.mappings_registry
    ):
      assert len(registry) == 1
      for (extension, extension_base_class) in created_extensions:
        if base_class == extension_base_class:
          registry_key = getattr(extension, attribute_name)
          assert issubclass(registry[registry_key], base_class)

  def test_load__vary_module_contents__one_of_each_extension__updates_count(
      self,
      concrete_external_loader_base_instance: ExternalLoaderBase,
      request: pytest.FixtureRequest,
  ) -> None:
    for extension_fixture in all_mocked_extensions:
      request.getfixturevalue(extension_fixture)

    concrete_external_loader_base_instance.load()

    assert concrete_external_loader_base_instance.loaded_extensions == len(
        all_mocked_extensions
    )

  def test_load__vary_module_contents__one_of_each_extension__logs_indicator(
      self,
      concrete_external_loader_base_instance: ExternalLoaderBase,
      request: pytest.FixtureRequest,
      capsys: pytest.CaptureFixture[str],
  ) -> None:
    for extension_fixture in all_mocked_extensions:
      request.getfixturevalue(extension_fixture)

    concrete_external_loader_base_instance.load()

    stdout, stderr = capsys.readouterr()
    assert stdout == (
        f(
            concrete_external_loader_base_instance.msg_fmt_load_indicator,
            concrete_external_loader_base_instance.loaded_extensions,
            nl=2,
        )
    )
    assert stderr == ""

  def test_load__no_module_contents__logs_no_indicator(
      self,
      concrete_external_loader_base_instance: ExternalLoaderBase,
      capsys: pytest.CaptureFixture[str],
  ) -> None:
    concrete_external_loader_base_instance.load()

    stdout, stderr = capsys.readouterr()
    assert concrete_external_loader_base_instance.loaded_extensions == 0
    assert stdout == ""
    assert stderr == ""
