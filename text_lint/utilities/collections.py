"""Collection utilities."""

from typing import List, TypeVar

TypeListContents = TypeVar("TypeListContents")


def unique_list(
    non_unique_list: List[TypeListContents]
) -> List[TypeListContents]:
  """Create a unique list from a list of objects.

  :param non_unique_list: A list of objects that is not known to be unique.
  :returns: A new list containing only unique objects from non_unique_list.
  """
  created_list: List[TypeListContents] = []
  for item in non_unique_list:
    if item not in created_list:
      created_list.append(item)
  return created_list
