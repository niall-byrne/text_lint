"""Shared mocking test fixtures."""
# pylint: disable=redefined-outer-name

from typing import Any, Callable
from unittest import mock

import pytest

AliasGenericMethod = Callable[..., Any]
AliasMethodMocker = Callable[["AliasGenericMethod"], mock.Mock]
AliasSpyOnMethod = Callable[["AliasGenericMethod"], mock.Mock]


@pytest.fixture
def method_mocker(monkeypatch: pytest.MonkeyPatch) -> "AliasMethodMocker":

  def create_mock(method: "AliasGenericMethod") -> mock.Mock:
    instance = getattr(method, "__self__")
    method_name = getattr(method, "__name__")
    mock_instance = mock.Mock(name=method_name)

    monkeypatch.setattr(
        instance,
        method_name,
        mock_instance,
    )
    return mock_instance

  return create_mock


@pytest.fixture
def spy_on_method(monkeypatch: pytest.MonkeyPatch) -> "AliasSpyOnMethod":

  def create_spy(method: "AliasGenericMethod") -> mock.Mock:
    instance = getattr(method, "__self__")
    method_name = getattr(method, "__name__")
    mock_instance = mock.Mock(name=method_name)

    def spy(*args: Any, **kwargs: Any) -> Any:
      mock_instance(*args, **kwargs)
      return method(*args, **kwargs)

    monkeypatch.setattr(
        instance,
        method_name,
        spy,
    )
    return mock_instance

  return create_spy
