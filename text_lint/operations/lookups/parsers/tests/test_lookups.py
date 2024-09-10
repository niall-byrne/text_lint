"""Test the lookup parser functions."""

import pytest
from text_lint.config import LOOKUP_SENTINEL
from text_lint.exceptions.lookups import LookupSyntaxInvalid
from text_lint.operations.lookups.bases.lookup_base import AliasLookupParams
from ..lookups import parse_lookup


class TestParseLookup:
  """Test the parse_lookup function."""

  @pytest.mark.parametrize(
      "value,expected_lookup,expected_params", [
          (LOOKUP_SENTINEL, LOOKUP_SENTINEL, []),
          ("1", "1", []),
          ("33", "33", []),
          ("A()", "A", []),
          ("A(1)", "A", [1]),
          ("aaaAAA(1)", "aaaAAA", [1]),
          ("aaaAAA(1,2,'bbBB')", "aaaAAA", [1, 2, "bbBB"]),
          ("~A(1)", "~A(1)", []),
      ]
  )
  def test__valid_parameters__vary_input__returns_name_and_params(
      self,
      value: str,
      expected_lookup: str,
      expected_params: "AliasLookupParams",
  ) -> None:
    result_lookup_name, result_params = parse_lookup(value)

    assert result_lookup_name == expected_lookup
    assert result_params == expected_params

  @pytest.mark.parametrize("value", ["A([)", "A(a)", "A({1:2})"])
  def test__invalid_parameters__vary_input__raises_exception(
      self,
      value: str,
  ) -> None:
    with pytest.raises(LookupSyntaxInvalid) as exc:
      parse_lookup(value)

    assert str(exc.value) == value

  @pytest.mark.parametrize("value", ["A", "1()"])
  def test__invalid_lookup_syntax__vary_input__raises_exception(
      self,
      value: str,
  ) -> None:
    with pytest.raises(LookupSyntaxInvalid) as exc:
      parse_lookup(value)

    assert str(exc.value) == value
