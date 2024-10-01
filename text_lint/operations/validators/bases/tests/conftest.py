"""Shared test fixtures for the validator base classes."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, Type

import pytest
from text_lint.utilities.translations import _
from .. import validator_base

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller.states import ValidatorState


@pytest.fixture
def mocked_validator_name() -> str:
  return "mocked_lookup_name"


@pytest.fixture
def concrete_validator_base_class() -> Type[validator_base.ValidatorBase]:

  class ConcreteValidator(validator_base.ValidatorBase):

    hint = _("mocked_hint")
    operation = "mocked_operation"

    def apply(self, state: "ValidatorState") -> None:
      """Mocked implementation."""

  return ConcreteValidator


@pytest.fixture
def concrete_validator_base_instance(
    concrete_validator_base_class: Type[validator_base.ValidatorBase],
    mocked_validator_name: str,
) -> validator_base.ValidatorBase:
  return concrete_validator_base_class(mocked_validator_name)
