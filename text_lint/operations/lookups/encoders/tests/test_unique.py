"""Test the UniqueEncoder class."""
import json
from typing import List

import pytest
from text_lint.utilities.collections import unique_list
from ..unique import UniqueEncoder
from .conftest import AliasSetupEncoderMock


class TestUniqueEncoder:
  """Test the UniqueEncoder class."""

  def test_initialize__inheritance(
      self,
      concrete_unique_encoder_instance: UniqueEncoder,
  ) -> None:
    assert isinstance(
        concrete_unique_encoder_instance,
        UniqueEncoder,
    )
    assert isinstance(
        concrete_unique_encoder_instance,
        json.JSONEncoder,
    )

  def test_encode__non_list_values__returns_json_encoded_values(
      self,
      concrete_unique_encoder_instance: UniqueEncoder,
      setup_encoder_mock: AliasSetupEncoderMock,
  ) -> None:
    setup_encoder_mock(method="encode", return_value=1)
    mocked_object = {"mocked": "object"}
    return_value = concrete_unique_encoder_instance.encode(mocked_object)

    assert return_value == 1

  def test_encode__single_dict_with_nested_lists__returns_unique_nested_lists(
      self,
      concrete_unique_encoder_instance: UniqueEncoder,
  ) -> None:
    mocked_object = {
        "strings": ["A", "A", "B"],
        "integers": [1, 2, 2],
        "nested": {
            "strings": ["A", "A", "B"],
            "integers": [1, 2, 2],
        }
    }

    return_value = concrete_unique_encoder_instance.encode(mocked_object)

    assert return_value == json.dumps(
        {
            "strings": ["A", "B"],
            "integers": [1, 2],
            "nested": {
                "strings": ["A", "B"],
                "integers": [1, 2],
            }
        }
    )

  @pytest.mark.parametrize(
      "mocked_list", ([["A", "A"]], [["A", "B"]], [["A", "A", "A", "B"]])
  )
  def test_encode__single_list_results__returns_unique_lists(
      self,
      concrete_unique_encoder_instance: UniqueEncoder,
      mocked_list: List[List[str]],
  ) -> None:
    return_value = concrete_unique_encoder_instance.encode(mocked_list)

    assert return_value == json.dumps([unique_list(mocked_list[0])])

  @pytest.mark.parametrize(
      "mocked_list", (
          [["A"], ["A", "A", "A"]],
          [["A", "B"], ["A", "B", "B"]],
          [["A", "B"], ["A", "A", "B"]],
      )
  )
  def test_encode__multiple_list_results__returns_unique_lists(
      self,
      concrete_unique_encoder_instance: UniqueEncoder,
      mocked_list: List[List[str]],
  ) -> None:
    return_value = concrete_unique_encoder_instance.encode(mocked_list)

    assert return_value == json.dumps([unique_list(mocked_list[0])])
