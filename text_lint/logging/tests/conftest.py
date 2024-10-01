"""Test fixtures for the text_lint logging modules."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from text_lint.logging import Logger
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.validators.bases.validator_base import ValidatorBase


@pytest.fixture
def mocked_assertion() -> mock.Mock:
  instance = mock.Mock(spec=AssertionBase)
  instance.name = "mocked assertion name"
  instance.operation = "mocked assertion operation"
  return instance


@pytest.fixture
def mocked_controller() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_validator() -> mock.Mock:
  instance = mock.Mock(spec=ValidatorBase)
  instance.operation = "mocked validation operation"
  instance.name = "mocked validation name"
  return instance


@pytest.fixture
def logger_instance(mocked_controller: mock.Mock) -> Logger:
  return Logger(mocked_controller)
