"""Shared test fixtures for the lookup encoder classes."""

import json
from typing import Any, Protocol
from unittest import mock

import pytest
from .. import lower
from .. import reversed as reversed_module
from .. import sorted as sorted_module
from .. import split, tree, unique, upper


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
def lower_case_encoder_instance() -> lower.LowerCaseEncoder:
  return lower.LowerCaseEncoder()


@pytest.fixture
def result_tree_encoder_instance() -> tree.ResultTreeEncoder:
  return tree.ResultTreeEncoder()


@pytest.fixture
def reversed_encoder_instance() -> reversed_module.ReversedEncoder:
  return reversed_module.ReversedEncoder()


@pytest.fixture
def sorted_encoder_instance() -> sorted_module.SortedEncoder:
  return sorted_module.SortedEncoder()


@pytest.fixture
def split_encoder_instance() -> split.SplitEncoder:
  return split.SplitEncoder()


@pytest.fixture
def unique_encoder_instance() -> unique.UniqueEncoder:
  return unique.UniqueEncoder()


@pytest.fixture
def upper_case_encoder_instance() -> upper.UpperCaseEncoder:
  return upper.UpperCaseEncoder()
