"""Shared test fixtures for the lookup operation base classes."""
# pylint: disable=redefined-outer-name

from typing import TYPE_CHECKING, Type
from unittest import mock

import pytest
from text_lint.utilities.translations import _
from .. import lookup_base, lookup_encoder_base

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState


@pytest.fixture
def mocked_encoder_class() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_json_module() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_lookup_name() -> str:
  return "mocked_lookup_name"


@pytest.fixture
def mocked_requesting_operation_name() -> str:
  return "mocked_requesting_operation_name"


@pytest.fixture
def mocked_lookup_expression() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_lookup_base_class() -> Type[lookup_base.LookupBase]:

  class ConcreteLookup(lookup_base.LookupBase):

    hint = _("mocked_hint_lookup")
    operation = "mocked_operation_lookup"

    def apply(self, state: "LookupState") -> None:
      """Mocked implementation."""

  return ConcreteLookup


@pytest.fixture
def concrete_lookup_encoder_base_class(
    mocked_encoder_class: mock.Mock,
    mocked_json_module: mock.Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> Type[lookup_encoder_base.LookupEncoderBase]:
  monkeypatch.setattr(
      lookup_encoder_base,
      "json",
      mocked_json_module,
  )

  class ConcreteLookupEncoder(lookup_encoder_base.LookupEncoderBase):

    encoder_class = mocked_encoder_class
    hint = _("mocked_hint_lookup_encoder")
    operation = "mocked_operation_lookup_encoder"

    def apply(self, state: "LookupState") -> None:
      """Mocked implementation."""

  return ConcreteLookupEncoder


@pytest.fixture
def concrete_lookup_base_instance(
    concrete_lookup_base_class: Type[lookup_base.LookupBase],
    mocked_lookup_name: str,
    mocked_requesting_operation_name: str,
    mocked_lookup_expression: mock.Mock,
) -> lookup_base.LookupBase:

  return concrete_lookup_base_class(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_requesting_operation_name,
  )


@pytest.fixture
def concrete_lookup_encoder_base_instance(
    concrete_lookup_encoder_base_class: Type[
        lookup_encoder_base.LookupEncoderBase],
    mocked_lookup_name: str,
    mocked_requesting_operation_name: str,
    mocked_lookup_expression: mock.Mock,
) -> lookup_encoder_base.LookupEncoderBase:

  return concrete_lookup_encoder_base_class(
      mocked_lookup_name,
      mocked_lookup_expression,
      mocked_requesting_operation_name,
  )
