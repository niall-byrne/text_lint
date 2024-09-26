"""Test the lookup module registry."""

import pytest
from .. import (
    LOOKUP_SENTINEL,
    CaptureLookup,
    CountLookup,
    DefaultLookup,
    GroupLookup,
    JsonLookup,
    LowerLookup,
    NoopLookup,
    ReversedLookup,
    SortedLookup,
    SplitLookup,
    UniqueLookup,
    UpperLookup,
    lookup_registry,
)


class TestLookupRegistry:
  """Test the lookup_registry default dictionary."""

  def test_default__returns_default_lookup(self) -> None:
    default_lookup_class = lookup_registry["non-existent-lookup-operation"]

    assert default_lookup_class == DefaultLookup

    del lookup_registry["non-existent-lookup-operation"]

  def test_sentinel__returns_noop_lookup(self) -> None:
    default_lookup_class = lookup_registry[LOOKUP_SENTINEL]

    assert default_lookup_class == NoopLookup

  @pytest.mark.parametrize("index", range(len(lookup_registry)))
  def test_vary_lookup__returns_correct_value(
      self,
      index: int,
  ) -> None:
    expected_operations = [
        NoopLookup.operation,
        CaptureLookup.operation,
        CountLookup.operation,
        GroupLookup.operation,
        JsonLookup.operation,
        LowerLookup.operation,
        NoopLookup.operation,
        ReversedLookup.operation,
        SortedLookup.operation,
        SplitLookup.operation,
        UniqueLookup.operation,
        UpperLookup.operation,
    ]
    lookup_registry_key = list(lookup_registry.keys())[index]

    retrieved_lookup_class = lookup_registry[lookup_registry_key]

    assert retrieved_lookup_class.operation == expected_operations[index]
