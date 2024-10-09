"""Test fixtures for the external loader base classes."""
# pylint: disable=redefined-outer-name

import abc
from random import randint
from types import ModuleType
from typing import Dict, List, Tuple, Type, cast
from unittest import mock

import pytest
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.lookups.bases.lookup_base import LookupBase
from text_lint.operations.validators.bases.validator_base import ValidatorBase
from text_lint.operations.validators.expressions.bases.expression_base import (
    ExpressionBase,
)
from .. import loader_base

AliasMockedRegistries = Dict[
    loader_base.AliasExtensionBaseClass,
    loader_base.AliasRegistry,
]

all_mocked_extensions = [
    "mocked_extension_assertion_class",
    "mocked_extension_expression_class",
    "mocked_extension_lookup_class",
    "mocked_extension_validator_class",
]


def attach_extension_to_mocked_module(
    mocked_modules: List[mock.Mock],
    mocked_class: loader_base.AliasExtensionBaseClass,
) -> None:
  index = randint(0, len(mocked_modules) - 1)
  setattr(mocked_modules[index], mocked_class.__name__, mocked_class)


@pytest.fixture
def mocked_modules() -> List[mock.Mock]:
  return [mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock()]


@pytest.fixture
def mocked_extension_assertion_class(
    mocked_modules: List[mock.Mock],
) -> Tuple[Type[AssertionBase], Type[AssertionBase]]:

  class MockAssertion(AssertionBase, abc.ABC):
    operation = "mocked_assertion"

  attach_extension_to_mocked_module(mocked_modules, MockAssertion)

  return MockAssertion, AssertionBase


@pytest.fixture
def mocked_extension_expression_class(
    mocked_modules: List[mock.Mock],
) -> Tuple[Type[ExpressionBase], Type[ExpressionBase]]:

  class MockExpression(ExpressionBase, abc.ABC):
    operator = "mocked_operator"

  attach_extension_to_mocked_module(mocked_modules, MockExpression)

  return MockExpression, ExpressionBase


@pytest.fixture
def mocked_extension_lookup_class(
    mocked_modules: List[mock.Mock],
) -> Tuple[Type[LookupBase], Type[LookupBase]]:

  class MockLookup(LookupBase, abc.ABC):
    operation = "mocked_lookup"

  attach_extension_to_mocked_module(mocked_modules, MockLookup)

  return MockLookup, LookupBase


@pytest.fixture
def mocked_extension_validator_class(
    mocked_modules: List[mock.Mock],
) -> Tuple[Type[ValidatorBase], Type[ValidatorBase]]:

  class MockValidator(ValidatorBase, abc.ABC):
    operation = "mocked_validators"

  attach_extension_to_mocked_module(mocked_modules, MockValidator)

  return MockValidator, ValidatorBase


@pytest.fixture
def mocked_registries() -> AliasMockedRegistries:
  return {
      AssertionBase: {},
      LookupBase: {},
      ValidatorBase: {},
      ExpressionBase: {},
  }


@pytest.fixture
def concrete_external_loader_base_class(
    mocked_modules: List[mock.Mock],
    mocked_registries: AliasMockedRegistries,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[loader_base.ExternalLoaderBase]:
  monkeypatch.setattr(
      loader_base,
      "assertion_registry",
      mocked_registries[AssertionBase],
  )
  monkeypatch.setattr(
      loader_base,
      "expressions_registry",
      mocked_registries[ExpressionBase],
  )
  monkeypatch.setattr(
      loader_base,
      "lookup_registry",
      mocked_registries[LookupBase],
  )
  monkeypatch.setattr(
      loader_base,
      "validator_registry",
      mocked_registries[ValidatorBase],
  )

  class ConcreteExternalLoader(loader_base.ExternalLoaderBase):
    msg_fmt_load_indicator = "concrete indicator: {0}"

    def load_modules(self) -> List[ModuleType]:
      return cast(List[ModuleType], mocked_modules)

  return ConcreteExternalLoader


@pytest.fixture
def concrete_external_loader_base_instance(
    concrete_external_loader_base_class: Type[loader_base.ExternalLoaderBase]
) -> loader_base.ExternalLoaderBase:
  return concrete_external_loader_base_class()
