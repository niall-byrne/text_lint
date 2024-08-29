"""Version information for text_lint."""

from typing import List, Tuple

from text_lint.exceptions.version import InvalidVersion

try:
  from importlib import metadata
except ImportError:  # pragma: no cover
  import importlib_metadata as metadata  # type: ignore[no-redef]

AliasVersionTuple = Tuple[int, int, int]


def string_to_version_tuple(version_string: str) -> AliasVersionTuple:
  """Convert dot separated version strings into a 3 element version tuples."""

  version_digits: List[int] = []

  if isinstance(version_string, str):
    try:
      version_digits = [int(digit) for digit in version_string.split(".")]
    except ValueError:
      pass

  if len(version_digits) != 3:
    raise InvalidVersion(version_string)

  return version_digits[0], version_digits[1], version_digits[2]


def version_tuple_to_string(version_tuple: AliasVersionTuple) -> str:
  """Convert a 3 element version tuple into a dot separated version string."""

  if not isinstance(version_tuple, tuple) or len(version_tuple) != 3:
    raise InvalidVersion(version_tuple)

  try:
    list(map(int, version_tuple))
  except ValueError as exc:
    raise InvalidVersion(version_tuple) from exc

  return ".".join(map(str, version_tuple))


APPLICATION_VERSION = string_to_version_tuple(metadata.version('text_lint'))
