""""Test fixtures for injecting lookup parameters."""
# pylint: disable=redefined-outer-name

from dataclasses import dataclass, field

import pytest
from text_lint.operations.lookups.bases.lookup_base import AliasLookupParams


@dataclass
class MockedLookupParamsContainer:
  value: "AliasLookupParams" = field(default_factory=lambda: [])


@pytest.fixture
def mocked_lookup_params(
    mocked_lookup_params_container: MockedLookupParamsContainer,
) -> "AliasLookupParams":
  return mocked_lookup_params_container.value


@pytest.fixture
def mocked_lookup_params_container() -> MockedLookupParamsContainer:
  return MockedLookupParamsContainer()
