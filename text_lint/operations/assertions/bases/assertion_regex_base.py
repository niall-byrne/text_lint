"""AssertionRegexBase class."""

import abc
import re
from typing import TYPE_CHECKING, Optional

from text_lint.operations.assertions.bases.assertion_base import AssertionBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.assertions.args.split import AliasYamlSplit

YAML_OPTIONS = """
optional: 'splits' will split the specified capture groups into more elements.
          (The default "separator" is any white space.)
optional: 'save' will store capture groups as save ids for validation processing.
          (The default behaviour is not to save any capture groups.)
"""


class AssertionRegexBase(AssertionBase, abc.ABC):
  """Parser regex based assertion base class."""

  __regex_flags = re.DOTALL

  def __init__(
      self,
      name: str,
      regex: str,
      save: Optional[str] = None,
      splits: Optional["AliasYamlSplit"] = None,
  ) -> None:
    self.regex = re.compile(regex, self.__regex_flags)
    super().__init__(name, save, splits)
