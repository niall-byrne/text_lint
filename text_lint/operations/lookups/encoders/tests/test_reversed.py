"""Test the ReversedEncoder class."""

import json
from typing import Any

from text_lint.__helpers__.lookups import result_reversing_test_cases
from ..reversed import ReversedEncoder
from .conftest import AliasSetupEncoderMock


class TestReversedEncoder:
  """Test the ReversedEncoder class."""

  def test_initialize__inheritance(
      self,
      reversed_encoder_instance: ReversedEncoder,
  ) -> None:
    assert isinstance(
        reversed_encoder_instance,
        ReversedEncoder,
    )
    assert isinstance(
        reversed_encoder_instance,
        json.JSONEncoder,
    )

  def test_encode__non_list_tuple_or_dict_value__pass_through(
      self,
      reversed_encoder_instance: ReversedEncoder,
      setup_encoder_mock: AliasSetupEncoderMock,
  ) -> None:
    setup_encoder_mock(method="encode", return_value=2)
    mocked_object = "non_list_tuple_or_dict_value"

    return_value = reversed_encoder_instance.encode(mocked_object)

    assert return_value == 2

  @result_reversing_test_cases
  def test_apply__vary_value__returns_expected_value(
      self,
      reversed_encoder_instance: ReversedEncoder,
      result: Any,
      expected: Any,
  ) -> None:
    return_value = reversed_encoder_instance.encode(result)

    assert return_value == json.dumps(expected)
