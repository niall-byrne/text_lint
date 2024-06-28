"""Collection utilities."""

from typing import List, TypeVar

TypeListContents = TypeVar("TypeListContents")


def unique_list(
    non_unique_list: List[TypeListContents]
) -> List[TypeListContents]:
  """Create a unique list from a list of items."""

  created_list: List[TypeListContents] = []
  for item in non_unique_list:
    if item not in created_list:
      created_list.append(item)
  return created_list
