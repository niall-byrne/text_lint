"""Test the translations utilities."""
import os
from unittest import mock

import text_lint.utilities.translations
from text_lint import config


class TestAliases:
  """Test the translations module's aliases."""

  def test_t__is_defined_correctly(
      self,
      translations: mock.Mock,
  ) -> None:
    # pylint: disable=comparison-with-callable
    assert text_lint.utilities.translations._ == translations

  def test_f__is_defined_correctly(self) -> None:
    assert text_lint.utilities.translations.f == (
        text_lint.utilities.translations.f_string
    )


class TestFString:
  """Test the f_string function."""

  def test_defaults__returns_correct_value(self,) -> None:
    received_string = text_lint.utilities.translations.f_string("string")

    assert received_string == "string"

  def test_defined_value__returns_correct_value(self,) -> None:
    received_string = text_lint.utilities.translations.f_string(
        "positional: {0}, key word: {key}", 1, key=2, nl=2
    )

    assert received_string == (
        "positional: {0}, key word: {key}{nl}{nl}".format(
            1, key=2, nl=config.NEW_LINE
        )
    )


class TestInitialize:
  """Test the initialize function."""

  @mock.patch.dict(
      text_lint.utilities.translations.__name__ + ".os.environ",
      {'LANG': 'ko_KR.UTF-8'},
      clear=True
  )
  def test_lang_is_set__lang_remains_unchanged(self) -> None:
    text_lint.utilities.translations.initialize()

    assert os.getenv("LANG") == "ko_KR.UTF-8"

  @mock.patch.dict(
      text_lint.utilities.translations.__name__ + ".os.environ", {}, clear=True
  )
  def test_lang_not_set__default_lang_used(
      self, mocked_locale: mock.Mock
  ) -> None:
    mocked_locale.getdefaultlocale.return_value = ['ko_KR.UTF-8']

    text_lint.utilities.translations.initialize()

    assert os.getenv("LANG") == mocked_locale.getdefaultlocale.return_value[0]

  def test_any_lang__returns_initialized_translations(
      self, mocked_gettext: mock.Mock
  ) -> None:
    return_value = text_lint.utilities.translations.initialize()

    mocked_gettext.translation.assert_called_once_with(
        "base",
        os.path.join(os.path.dirname(text_lint.__file__), "locales"),
        fallback=True,
    )
    assert return_value == mocked_gettext.translation.return_value
