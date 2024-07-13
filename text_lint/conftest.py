"""Shared test fixtures for the text_lint project."""
# pylint: disable=redefined-outer-name

import sys
from importlib import import_module
from unittest import mock

import pytest

TRANSLATION_MARKER = "gettext > "

pytest_plugins = [
    "text_lint.__fixtures__.lookup_expressions",
    "text_lint.__fixtures__.mocks",
]

mocked_t = mock.Mock(side_effect=lambda text: TRANSLATION_MARKER + text)


def global_mocks() -> None:
  import_module("text_lint.utilities.translations")
  setattr(
      sys.modules["text_lint.utilities.translations"],
      "_",
      mocked_t,
  )


@pytest.fixture
def translations() -> mock.Mock:
  return mocked_t


global_mocks()
