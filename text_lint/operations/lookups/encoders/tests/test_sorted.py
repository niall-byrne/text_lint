"""Test the SortedEncoder class."""
import json
from typing import Any

from text_lint.__helpers__.lookups import result_sorting_test_cases
from ..sorted import SortedEncoder
from .conftest import AliasSetupEncoderMock


class TestSortedEncoder:
  """Test the SortedEncoder class."""

  def test_initialize__inheritance(
      self,
      concrete_sorted_encoder_instance: SortedEncoder,
  ) -> None:
    assert isinstance(
        concrete_sorted_encoder_instance,
        SortedEncoder,
    )
    assert isinstance(
        concrete_sorted_encoder_instance,
        json.JSONEncoder,
    )

  def test_encode__non_list_tuple_or_dict_value__pass_through(
      self,
      concrete_sorted_encoder_instance: SortedEncoder,
      setup_encoder_mock: AliasSetupEncoderMock,
  ) -> None:
    setup_encoder_mock(method="encode", return_value=2)
    mocked_object = "non_list_tuple_or_dict_value"

    return_value = concrete_sorted_encoder_instance.encode(mocked_object)

    assert return_value == 2

  @result_sorting_test_cases
  def test_apply__vary_value__returns_expected_value(
      self,
      concrete_sorted_encoder_instance: SortedEncoder,
      result: Any,
      expected: Any,
  ) -> None:
    return_value = concrete_sorted_encoder_instance.encode(result)

    assert return_value == json.dumps(expected)
