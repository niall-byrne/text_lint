"""File type for CLI command arguments."""

import os


def file_type(filename: str) -> str:
  """Validate a specified filename actually exists."""

  if os.path.exists(filename):
    return os.path.abspath(filename)
  raise FileNotFoundError(filename)
