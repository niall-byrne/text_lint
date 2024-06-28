"""Test the LowerCaseEncoder class."""
import json

from ..lower import LowerCaseEncoder
from .conftest import AliasSetupEncoderMock


class TestLowerCaseEncoder:
  """Test the LowerCaseEncoder class."""

  def test_initialize__inheritance(
      self,
      concrete_lower_case_encoder_instance: LowerCaseEncoder,
  ) -> None:
    assert isinstance(
        concrete_lower_case_encoder_instance,
        LowerCaseEncoder,
    )
    assert isinstance(
        concrete_lower_case_encoder_instance,
        json.JSONEncoder,
    )

  def test_encode__non_string_value__pass_through(
      self,
      concrete_lower_case_encoder_instance: LowerCaseEncoder,
      setup_encoder_mock: AliasSetupEncoderMock,
  ) -> None:
    setup_encoder_mock(method="encode", return_value=1)
    mocked_object = {
        "UPPER": "CASE",
        "lower": "case",
        "nested": {
            "object": "here"
        }
    }

    return_value = concrete_lower_case_encoder_instance.encode(mocked_object)

    assert return_value == 1

  def test_encode__converts_case_as_expected(
      self,
      concrete_lower_case_encoder_instance: LowerCaseEncoder,
  ) -> None:
    mocked_object = {
        "UPPER": "CASE",
        "lower": "case",
        "nested": {
            "object": "here"
        }
    }

    return_value = concrete_lower_case_encoder_instance.encode(mocked_object)

    assert return_value == json.dumps(
        {
            "upper": "case",
            "lower": "case",
            "nested": {
                "object": "here"
            }
        }
    )
