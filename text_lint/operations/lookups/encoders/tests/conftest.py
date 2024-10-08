"""Shared test fixtures for the lookup encoder classes."""

import json
from typing import Any, Protocol
from unittest import mock

import pytest
from .. import lower, tree, unique, upper
from ..reversed import ReversedEncoder
from ..sorted import SortedEncoder


class AliasSetupEncoderMock(Protocol):

  def __call__(self, method: str, return_value: Any) -> mock.Mock:
    ...


@pytest.fixture
def setup_encoder_mock(
    monkeypatch: pytest.MonkeyPatch,
) -> AliasSetupEncoderMock:

  def setup(method: str, return_value: Any) -> mock.Mock:
    mocked_encoder = mock.Mock(return_value=return_value)
    monkeypatch.setattr(json.JSONEncoder, method, mocked_encoder)
    return mocked_encoder

  return setup


@pytest.fixture
def concrete_lower_case_encoder_instance() -> lower.LowerCaseEncoder:
  return lower.LowerCaseEncoder()


@pytest.fixture
def concrete_result_tree_encoder_instance() -> tree.ResultTreeEncoder:
  return tree.ResultTreeEncoder()


@pytest.fixture
def concrete_reversed_encoder_instance() -> ReversedEncoder:
  return ReversedEncoder()


@pytest.fixture
def concrete_sorted_encoder_instance() -> SortedEncoder:
  return SortedEncoder()


@pytest.fixture
def concrete_unique_encoder_instance() -> unique.UniqueEncoder:
  return unique.UniqueEncoder()


@pytest.fixture
def concrete_upper_case_encoder_instance() -> upper.UpperCaseEncoder:
  return upper.UpperCaseEncoder()
