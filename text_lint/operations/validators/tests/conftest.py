"""Shared test fixtures for the validator classes."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, List
from unittest import mock

import pytest
from text_lint.operations.validators.bases.validator_base import ValidatorBase
from .. import (
    validate_combine,
    validate_debug,
    validate_equal,
    validate_expression,
    validate_membership,
    validate_not_equal,
    validate_not_membership,
)
# pylint: disable=wildcard-import,unused-wildcard-import
from .scenarios import *

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.__helpers__.operations import AliasParameterDefinitions


@pytest.fixture
def base_parameter_definitions() -> "AliasParameterDefinitions":
  return {
      "name": ValidatorBase.Parameters.name,
  }


@pytest.fixture
def mocked_result_tree_name() -> str:
  return "mocked_result_tree_name"


@pytest.fixture
def mocked_state() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_validator_name() -> str:
  return "mocked_validator_name"


@pytest.fixture
def validate_combine_instance(
    mocked_lookup_expression_set_a: List[str],
    mocked_result_tree_name: str,
    mocked_validator_name: str,
) -> validate_combine.ValidateCombine:
  return validate_combine.ValidateCombine(
      mocked_validator_name,
      new_saved=mocked_result_tree_name,
      saved=mocked_lookup_expression_set_a,
  )


@pytest.fixture
def validate_debug_instance(
    mocked_lookup_expression_set_a: List[str],
    mocked_validator_name: str,
) -> validate_debug.ValidateDebug:
  return validate_debug.ValidateDebug(
      mocked_validator_name,
      saved=mocked_lookup_expression_set_a,
  )


@pytest.fixture
def validate_equal_instance(
    mocked_lookup_expression_set_a: List[str],
    mocked_lookup_expression_set_b: List[str],
    mocked_validator_name: str,
) -> validate_equal.ValidateEqual:
  return validate_equal.ValidateEqual(
      mocked_validator_name,
      saved_a=mocked_lookup_expression_set_a,
      saved_b=mocked_lookup_expression_set_b,
  )


@pytest.fixture
def validate_expression_instance(
    mocked_lookup_expression_set_a: List[str],
    mocked_lookup_expression_set_b: List[str],
    mocked_result_tree_name: str,
    mocked_validator_name: str,
    request: pytest.FixtureRequest,
) -> validate_expression.ValidateExpression:
  return validate_expression.ValidateExpression(
      mocked_validator_name,
      operator=request.param,
      new_saved=mocked_result_tree_name,
      saved_a=mocked_lookup_expression_set_a,
      saved_b=mocked_lookup_expression_set_b,
  )


@pytest.fixture
def validate_membership_instance(
    mocked_lookup_expression_set_a: List[str],
    mocked_lookup_expression_set_b: List[str],
    mocked_validator_name: str,
) -> validate_membership.ValidateMembership:
  return validate_membership.ValidateMembership(
      mocked_validator_name,
      saved_container=mocked_lookup_expression_set_a,
      saved_value=mocked_lookup_expression_set_b,
  )


@pytest.fixture
def validate_not_equal_instance(
    mocked_lookup_expression_set_a: List[str],
    mocked_lookup_expression_set_b: List[str],
    mocked_validator_name: str,
) -> validate_not_equal.ValidateNotEqual:
  return validate_not_equal.ValidateNotEqual(
      mocked_validator_name,
      saved_a=mocked_lookup_expression_set_a,
      saved_b=mocked_lookup_expression_set_b,
  )


@pytest.fixture
def validate_not_membership_instance(
    mocked_lookup_expression_set_a: List[str],
    mocked_lookup_expression_set_b: List[str],
    mocked_validator_name: str,
) -> validate_not_membership.ValidateNotMembership:
  return validate_not_membership.ValidateNotMembership(
      mocked_validator_name,
      saved_container=mocked_lookup_expression_set_a,
      saved_value=mocked_lookup_expression_set_b,
  )
