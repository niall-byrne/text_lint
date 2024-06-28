"""Test fixtures for the parser rules base classes."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, Type
from unittest import mock

import pytest
from text_lint.utilities.translations import _
from .. import rule_base, rule_regex_base

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller


@pytest.fixture
def mocked_result_class() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_implementation() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_rule_base_class(
    mocked_implementation: mock.Mock,
    mocked_result_class: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[rule_base.RuleBase]:
  monkeypatch.setattr(
      rule_base,
      "ResultTree",
      mocked_result_class,
  )

  class ConcreteRule(rule_base.RuleBase):
    """Concrete rule base class."""

    hint = _("a concrete hint")
    operation = "a concrete operation"

    def apply(
        self,
        controller: "Controller",
    ) -> None:
      mocked_implementation(controller)
      self.matches.append(mock.Mock())

  return ConcreteRule


@pytest.fixture
def concrete_rule_base_instance(
    concrete_rule_base_class: Type[rule_base.RuleBase],
) -> rule_base.RuleBase:
  instance = concrete_rule_base_class(
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
def concrete_rule_regex_base_class() -> Type[rule_regex_base.RuleRegexBase]:

  class ConcreteRuleRegex(rule_regex_base.RuleRegexBase):
    """Concrete regex rule base class."""

    hint = _("a concrete regex hint")
    operation = "a concrete operation"

    def apply(
        self,
        controller: "Controller",
    ) -> None:
      """Mocked implementation."""

  return ConcreteRuleRegex


@pytest.fixture
def concrete_rule_regex_base_instance(
    concrete_rule_regex_base_class: Type[rule_regex_base.RuleRegexBase],
) -> rule_regex_base.RuleRegexBase:
  instance = concrete_rule_regex_base_class(
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
