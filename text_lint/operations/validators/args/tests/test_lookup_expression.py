"""Test the LookupExpression class."""
import pytest
from text_lint.config import (
    LOOKUP_SENTINEL,
    LOOKUP_SEPERATOR,
    LOOKUP_STATIC_VALUE_MARKER,
)
from text_lint.operations.lookups import CaptureLookup, NoopLookup, UpperLookup
from ..lookup_expression import LookupExpression


class TestLookupExpression:
  """Test the LookupExpression class."""

  def test_initialize__source_only__attributes(self) -> None:
    mock_lookup = "source_name"

    instance = LookupExpression(mock_lookup)

    assert instance.name == mock_lookup
    assert instance.source == "source_name"
    assert instance.lookups == [LOOKUP_SENTINEL]

  def test_initialize__valid_lookup__attributes(self) -> None:
    mock_lookup = LOOKUP_SEPERATOR.join(
        [
            "source_name",
            NoopLookup.operation,
            UpperLookup.operation,
        ]
    )

    instance = LookupExpression(mock_lookup)

    assert instance.name == mock_lookup
    assert instance.source == "source_name"
    assert instance.lookups == [
        NoopLookup.operation,
        UpperLookup.operation,
    ]

  def test_initialize__valid_lookup_with_index__attributes(self) -> None:
    mock_lookup = LOOKUP_SEPERATOR.join(
        [
            "source_name",
            NoopLookup.operation,
            UpperLookup.operation,
            "1",
        ]
    )

    instance = LookupExpression(mock_lookup)

    assert instance.name == mock_lookup
    assert instance.source == "source_name"
    assert instance.lookups == [
        NoopLookup.operation,
        UpperLookup.operation,
        "1",
    ]

  def test_initialize__valid_lookup_with_name_marker__attributes(self) -> None:
    mock_lookup = LOOKUP_SEPERATOR.join(
        [
            "source_name",
            NoopLookup.operation,
            UpperLookup.operation,
            LOOKUP_STATIC_VALUE_MARKER + "mock_value",
        ]
    )

    instance = LookupExpression(mock_lookup)

    assert instance.name == mock_lookup
    assert instance.source == "source_name"
    assert instance.lookups == [
        NoopLookup.operation,
        UpperLookup.operation,
        LOOKUP_STATIC_VALUE_MARKER + "mock_value",
    ]

  def test_initialize__unknown_lookup__attributes(self) -> None:
    mock_lookup = LOOKUP_SEPERATOR.join(
        [
            "source_name",
            NoopLookup.operation,
            UpperLookup.operation,
            "unknown_lookup",
        ]
    )

    instance = LookupExpression(mock_lookup)

    assert instance.name == mock_lookup
    assert instance.source == "source_name"
    assert instance.lookups == [
        NoopLookup.operation,
        UpperLookup.operation,
        "unknown_lookup",
    ]

  def test_initialize__invalid_lookup_sequence__raises_exception(self) -> None:
    mock_lookup = LOOKUP_SEPERATOR.join(
        [
            "source_name",
            UpperLookup.operation,
            CaptureLookup.operation,
        ]
    )

    with pytest.raises(ValueError) as exc:
      LookupExpression(mock_lookup)

    assert str(exc.value) == \
        "Transformations belong at the end of a lookup expression."
