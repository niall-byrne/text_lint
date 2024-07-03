"""Shared test fixtures for the validator base classes."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, Callable, List, Type
from unittest import mock

import pytest
from text_lint.utilities.translations import _
from .. import validator_base, validator_comparison_base

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import ValidatorState
  from text_lint.results.forest import AliasLookupResult


@pytest.fixture
def mocked_comparison() -> mock.Mock:
  return mock.Mock(return_value=True)


@pytest.fixture
def mocked_state() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_validator_name() -> str:
  return "mocked_validator_name"


@pytest.fixture
def concrete_validator_base_class() -> Type[validator_base.ValidatorBase]:

  class ConcreteValidator(validator_base.ValidatorBase):

    hint = _("mocked_validator_base_hint")
    operation = "mocked_validator_base_operation"
    yaml_example = "mocked_validator_base_yaml_example"

    def apply(self, state: "ValidatorState") -> None:
      """Mocked implementation."""

  return ConcreteValidator


@pytest.fixture
def concrete_validator_base_instance(
    concrete_validator_base_class: Type[validator_base.ValidatorBase],
    mocked_validator_name: str,
) -> validator_base.ValidatorBase:
  return concrete_validator_base_class(mocked_validator_name)


@pytest.fixture
def concrete_validator_comparison_base_class(
    mocked_comparison: Callable[[], bool],
) -> Type[validator_comparison_base.ValidationComparisonBase]:

  class ConcreteValidatorComparison(
      validator_comparison_base.ValidationComparisonBase
  ):
    hint = _("mocked_validator_comparison_base_hint")
    operation = "mocked_validator_comparison_base_operation"
    yaml_example = "mocked_validator_comparison_base_yaml_example"

    msg_fmt_comparison_failure = _("'{0}' comparison '{1}'")
    msg_fmt_comparison_success = _("MOCKED: '{0}' and '{1}'")

    def comparison(
        self,
        result_a: "AliasLookupResult",
        result_b: "AliasLookupResult",
    ) -> bool:
      return mocked_comparison()

  return ConcreteValidatorComparison


@pytest.fixture
def concrete_validator_comparison_base_instance(
    concrete_validator_comparison_base_class: Type[
        validator_comparison_base.ValidationComparisonBase],
    mocked_validator_name: str,
    mocked_lookup_expression_set_a: List[str],
    mocked_lookup_expression_set_b: List[str],
) -> validator_comparison_base.ValidationComparisonBase:
  return concrete_validator_comparison_base_class(
      mocked_validator_name,
      saved_a=mocked_lookup_expression_set_a,
      saved_b=mocked_lookup_expression_set_b,
  )
