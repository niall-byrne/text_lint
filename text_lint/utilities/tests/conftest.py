"""Shared test fixtures for the text_lint utilities tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from .. import translations


@pytest.fixture
def mocked_gettext(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(translations, "gettext", instance)
  return instance


@pytest.fixture
def mocked_locale(monkeypatch: pytest.MonkeyPatch) -> mock.Mock:
  instance = mock.Mock()
  monkeypatch.setattr(translations, "locale", instance)
  return instance
