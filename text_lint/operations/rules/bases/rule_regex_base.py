"""RuleRegexBase class."""

import abc
import re
from typing import TYPE_CHECKING, Optional

from text_lint.operations.rules.bases.rule_base import RuleBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.rules.args.split import AliasYamlSplit

YAML_OPTIONS = """
optional: 'splits' will split the specified capture groups into more elements.
          (The default "separator" is any white space.)
optional: 'save' will store the the entire string for validation processing.
          (This defaults to not saving any result.)
"""


class RuleRegexBase(RuleBase, abc.ABC):
  """Parser regex based rule base class."""

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
