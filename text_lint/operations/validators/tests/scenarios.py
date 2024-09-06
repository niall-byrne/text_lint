"""Test scenarios for the validator operator tests."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest

__all__ = (
    "scenario__comparison__lookup_results_equal",
    "scenario__comparison__lookup_results_not_equal",
    "scenario__comparison__lookup_results_invalid_membership",
    "scenario__comparison__lookup_results_membership",
    "scenario__comparison__lookup_results_not_membership",
)


@pytest.fixture
def scenario__comparison__lookup_results_equal(mocked_state: mock.Mock) -> None:
  mocked_state.lookup_expression.side_effect = (
      "result_0",
      "result_0",
      "result_1",
      "result_1",
  )


@pytest.fixture
def scenario__comparison__lookup_results_not_equal(
    mocked_state: mock.Mock
) -> None:
  mocked_state.lookup_expression.side_effect = (
      "result_0",
      "result_1",
      "result_0",
      "result_1",
  )


@pytest.fixture
def scenario__comparison__lookup_results_invalid_membership(
    mocked_state: mock.Mock
) -> None:
  mocked_state.lookup_expression.side_effect = (
      "result_0",
      ["result_1"],
      "result_0",
      ["result_1"],
  )


@pytest.fixture
def scenario__comparison__lookup_results_membership(
    mocked_state: mock.Mock
) -> None:
  mocked_state.lookup_expression.side_effect = (
      ["result_0"],
      "result_0",
      ["result_1"],
      "result_1",
  )


@pytest.fixture
def scenario__comparison__lookup_results_not_membership(
    mocked_state: mock.Mock
) -> None:
  mocked_state.lookup_expression.side_effect = (
      ["result_0"],
      "result_1",
      ["result_1"],
      "result_0",
  )
