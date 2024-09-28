"""DeferredLinterSettings class."""

from typing import TYPE_CHECKING, Type

from .bases.deferred_base import DeferredModuleLoaderBase

if TYPE_CHECKING:  # no cover
  from text_lint.linter.settings import LinterSettings as LinterSettingsType


class DeferredLinterSettings(
    DeferredModuleLoaderBase[Type["LinterSettingsType"]]
):
  """Deferred LinterSettings loader."""

  module_path = "text_lint.linter.settings"
  module_attribute = "LinterSettings"


deferred_linter_settings = DeferredLinterSettings()
