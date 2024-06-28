"""Test the UpperCaseEncoder class."""
import json

from ..upper import UpperCaseEncoder
from .conftest import AliasSetupEncoderMock


class TestUpperCaseEncoder:
  """Test the UpperCaseEncoder class."""

  def test_initialize__inheritance(
      self,
      upper_case_encoder_instance: UpperCaseEncoder,
  ) -> None:
    assert isinstance(
        upper_case_encoder_instance,
        UpperCaseEncoder,
    )
    assert isinstance(
        upper_case_encoder_instance,
        json.JSONEncoder,
    )

  def test_encode__non_string_value__pass_through(
      self,
      upper_case_encoder_instance: UpperCaseEncoder,
      setup_encoder_mock: AliasSetupEncoderMock,
  ) -> None:
    setup_encoder_mock(method="encode", return_value=2)
    mocked_object = {
        "UPPER": "CASE",
        "lower": "case",
        "nested": {
            "object": "HERE"
        }
    }

    return_value = upper_case_encoder_instance.encode(mocked_object)

    assert return_value == 2

  def test_encode__converts_case_as_expected(
      self,
      upper_case_encoder_instance: UpperCaseEncoder,
  ) -> None:
    mocked_object = {
        "UPPER": "CASE",
        "lower": "case",
        "nested": {
            "object": "HERE"
        }
    }

    return_value = upper_case_encoder_instance.encode(mocked_object)

    assert return_value == json.dumps(
        {
            "UPPER": "CASE",
            "LOWER": "CASE",
            "NESTED": {
                "OBJECT": "HERE"
            }
        }
    )
