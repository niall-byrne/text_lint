"""String splits assertion operation YAML argument definitions."""

from typing import Any, Dict, List, Optional

from text_lint.operations.mixins.parameter_validation import (
    ParameterValidationMixin,
    validator_factories,
)
from text_lint.utilities.translations import _

AliasYamlSplit = Optional[List[Dict[str, Any]]]


class SplitArgs:
  """String splits YAML argument definitions."""

  msg_fmt_invalid_splits = _(
      "The value '{0}' is not a valid set of string splits"
  )

  def __init__(self, splits: List["Split"]) -> None:
    """Initialize SplitArgs instances.

    :param splits: A list of string split definitions.
    """
    self.splits = splits

  @classmethod
  def create(cls, yaml_input: Optional[AliasYamlSplit]) -> "SplitArgs":
    """Create an instance from YAML input.

    :param yaml_input: Optional list of YAML text splitting configurations.
    :returns: A new SplitArgs instance configured with this YAML.
    :raises: TypeError
    """
    created_splits = []
    if yaml_input is not None:

      if not isinstance(yaml_input, (list, tuple)):
        raise TypeError(cls.msg_fmt_invalid_splits.format(yaml_input))

      for yaml_split in yaml_input:
        created_splits.append(Split(**yaml_split))

    return cls(splits=created_splits)

  def as_dict(self) -> Dict[int, Optional[str]]:
    """Generate a dictionary representation of the string splits.

    :returns: A dictionary representation of the string splits.
    """
    return {split.group: split.separator for split in self.splits}


class Split(ParameterValidationMixin):
  """String split definition."""

  def __init__(
      self,
      group: int,
      separator: Optional[str] = None,
  ) -> None:
    """Initialize Split instances.

    It should be noted that by default text is split by whitespace unless a
    seperator is defined.

    :param group: The index of the regex capture group this split applies to.
    :param separator: An optional (non-default) seperator string.
    :raises: TypeError
    """
    self.group = group
    self.separator = separator
    self.validate_parameters()

  class Parameters:
    """Validation configuration for this split's parameters."""

    group = {
        "type": int,
        "validators": [validator_factories.create_is_greater_than_or_equal(1)],
    }
    separator = {"type": str, "optional": True}
