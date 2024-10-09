"""File type for CLI command arguments."""

import os


def file_type(filename: str) -> str:
  """Validate a specified filename actually exists."""

  if os.path.exists(filename):
    if os.path.isfile(filename):
      return os.path.abspath(filename)
    raise IsADirectoryError(filename)
  raise FileNotFoundError(filename)
