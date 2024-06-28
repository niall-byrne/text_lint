"""Test the collections utilities."""

from typing import List

import pytest
from text_lint.utilities import collections


class TestUniqueList:
  """Test the translations module's aliases."""

  def test_unique_list__empty_list__returns_empty_list(self) -> None:
    return_value: List[None] = collections.unique_list([])

    # pylint: disable=use-implicit-booleaness-not-comparison
    assert return_value == []

  @pytest.mark.parametrize(
      "mocked_list", (
          ["A", "B"],
          ["A", "A", "B"],
          ["A", "A", "A", "B"],
          ["A", "A", "A", "B", "B"],
      )
  )
  def test_unique_list__vary_list_of_str__returns_unique_list(
      self,
      mocked_list: List[str],
  ) -> None:
    return_value = collections.unique_list(mocked_list)

    assert return_value == ["A", "B"]

  @pytest.mark.parametrize(
      "mocked_list", (
          [1, 2],
          [1, 1, 2],
          [1, 1, 1, 2],
          [1, 1, 1, 2, 2],
      )
  )
  def test_unique_list__vary_list_of_int__returns_unique_list(
      self,
      mocked_list: List[int],
  ) -> None:
    return_value = collections.unique_list(mocked_list)

    assert return_value == [1, 2]
