"""Directory type for CLI command arguments."""

import os


def directory_type(path: str) -> str:
  """Validate a specified directory actually exists.

  :param path: The path to validate.
  :returns: The absolute validated path.
  """
  if os.path.exists(path):
    if os.path.isdir(path):
      return os.path.abspath(path)
    raise NotADirectoryError(path)
  raise FileNotFoundError(path)
