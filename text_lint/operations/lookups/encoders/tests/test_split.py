"""Test the SplitEncoder class."""
import json
from copy import deepcopy
from typing import Any

from text_lint.__helpers__.lookups import result_splitting_test_cases
from ..split import SplitEncoder


class TestSplitEncoder:
  """Test the SplitEncoder class."""

  def test_initialize__inheritance(
      self,
      split_encoder_instance: SplitEncoder,
  ) -> None:
    assert isinstance(
        split_encoder_instance,
        SplitEncoder,
    )
    assert isinstance(
        split_encoder_instance,
        json.JSONEncoder,
    )

  def test_encode__non_splittable_value__valid_seperator__pass_through(
      self,
      split_encoder_instance: SplitEncoder,
  ) -> None:
    split_encoder_instance.seperator = " "

    return_value = split_encoder_instance.encode(None)

    assert return_value == 'null'

  @result_splitting_test_cases
  def test_encode__vary_value__vary_seperator__returns_expected_value(
      self,
      split_encoder_instance: SplitEncoder,
      result: Any,
      seperator: Any,
      expected: Any,
  ) -> None:
    split_encoder_instance.seperator = seperator

    return_value = split_encoder_instance.encode(deepcopy(result))

    assert return_value == json.dumps(expected)
