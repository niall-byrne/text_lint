"""AssertionRegexBase class."""

import abc
import re
from typing import TYPE_CHECKING, Optional

from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.assertions.args.split import AliasYamlSplit

YAML_ASSERTION_REGEX_EXAMPLE_OPTIONS = _(
    """  - 'save' will store capture groups as save ids for validation.
    (The default behaviour is not to save any capture groups.)
  - 'splits' will split the specified capture groups into more elements.
    (The default 'separator' is any white space.)"""
)


class AssertionRegexBase(AssertionBase, abc.ABC):
  """Regex based assertion operation base class."""

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
