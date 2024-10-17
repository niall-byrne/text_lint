"""Shared operations test fixtures."""
# pylint: disable=redefined-outer-name

from unittest import mock

import pytest
from text_lint.operations.mixins.parameter_validation import (
    ParameterValidationMixin,
)


@pytest.fixture
def validate_parameters_spy(
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
) -> mock.Mock:
  klass = request.param
  method_name = "validate_parameters"

  method = getattr(klass, method_name)
  validate_parameters_spy = mock.Mock(name=method.__name__)

  def spy(klass_instance: ParameterValidationMixin) -> None:
    validate_parameters_spy(klass_instance)
    method(klass_instance)

  monkeypatch.setattr(
      klass,
      method_name,
      spy,
  )

  return validate_parameters_spy
