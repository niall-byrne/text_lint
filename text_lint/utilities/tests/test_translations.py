"""Test the translations utilities."""

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
