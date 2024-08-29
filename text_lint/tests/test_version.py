"""Test the text_lint version module."""
from typing import Any

import pytest
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.version import InvalidVersion
from text_lint.version import (
    AliasVersionTuple,
    string_to_version_tuple,
    version_tuple_to_string,
)


class TestStringToVersionTuple:
  """Test the to_version_tuple function."""

  @pytest.mark.parametrize(
      "version_string,expected_tuple",
      [
          ["0.0.3", (0, 0, 3)],
          ["0.2.3", (0, 2, 3)],
          ["1.2.3", (1, 2, 3)],
      ],
      ids=str,
  )
  def test_valid_version_string__creates_correct_tuple(
      self,
      version_string: str,
      expected_tuple: AliasVersionTuple,
  ) -> None:
    created_version_tuple = string_to_version_tuple(version_string)

    assert created_version_tuple == expected_tuple

  @pytest.mark.parametrize(
      "version_string",
      ["0", "0.0", "A.B.C", 0],
      ids=str,
  )
  def test_invalid_version_string__raises_exception(
      self,
      version_string: Any,
  ) -> None:
    with pytest.raises(InvalidVersion) as exc:
      string_to_version_tuple(version_string)

    assert str(exc.value) == \
        InvalidVersion.msg_fmt_invalid.format(version_string)
    assert_is_translated(InvalidVersion.msg_fmt_invalid)


class TestVersionTupleToString:
  """Test the version_tuple_to_string function."""

  @pytest.mark.parametrize(
      "version_tuple,expected_string",
      [
          [(0, 0, 3), "0.0.3"],
          [(0, 2, 3), "0.2.3"],
          [(1, 2, 3), "1.2.3"],
      ],
      ids=str,
  )
  def test_valid_version_tuple__creates_correct_string(
      self,
      version_tuple: AliasVersionTuple,
      expected_string: str,
  ) -> None:
    created_version_string = version_tuple_to_string(version_tuple)

    assert created_version_string == expected_string

  @pytest.mark.parametrize(
      "version_tuple",
      [(0,), (0, 0), ("A", "B", "C"), "A"],
      ids=str,
  )
  def test_invalid_version_tuple__raises_exception(
      self,
      version_tuple: Any,
  ) -> None:
    with pytest.raises(InvalidVersion) as exc:
      version_tuple_to_string(version_tuple)

    assert str(exc.value) == \
        InvalidVersion.msg_fmt_invalid.format(version_tuple)
    assert_is_translated(InvalidVersion.msg_fmt_invalid)
