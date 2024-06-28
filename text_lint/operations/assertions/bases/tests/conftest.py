"""Test fixtures for the parser assertions base classes."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, List, Type
from unittest import mock

import pytest
from text_lint.utilities.translations import _
from .. import assertion_base, assertion_regex_base

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller


@pytest.fixture
def mocked_results() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_result_class() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_assertion_base_class(
    mocked_implementation: mock.Mock,
    mocked_result_class: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[assertion_base.AssertionBase]:
  monkeypatch.setattr(
      assertion_base,
      "ResultTree",
      mocked_result_class,
  )

  class ConcreteAssertion(assertion_base.AssertionBase):
    """Concrete assertion base class."""

    hint = _("a concrete hint")
    operation = "a concrete operation"

    def apply(
        self,
        controller: "Controller",
    ) -> None:
      mocked_implementation(controller)

  return ConcreteAssertion


@pytest.fixture
def concrete_assertion_base_instance(
    concrete_assertion_base_class: Type[assertion_base.AssertionBase],
) -> assertion_base.AssertionBase:
  instance = concrete_assertion_base_class(
      name="concrete name",
      save="save_id",
      splits=[
          {
              "group": 1,
              "separator": None
          },
      ]
  )
  return instance


@pytest.fixture
def concrete_assertion_regex_base_class(
) -> Type[assertion_regex_base.AssertionRegexBase]:

  class ConcreteAssertionRegex(assertion_regex_base.AssertionRegexBase):
    """Concrete regex assertion base class."""

    hint = _("a concrete regex hint")
    operation = "a concrete operation"

    def apply(
        self,
        controller: "Controller",
    ) -> None:
      """Mocked implementation."""

  return ConcreteAssertionRegex


@pytest.fixture
def concrete_assertion_regex_base_instance(
    concrete_assertion_regex_base_class: Type[
        assertion_regex_base.AssertionRegexBase],
) -> assertion_regex_base.AssertionRegexBase:
  instance = concrete_assertion_regex_base_class(
      name="concrete name",
      regex=r'[a-z]+',
      save="save_id",
      splits=[
          {
              "group": 1,
              "separator": None
          },
      ]
  )
  return instance
