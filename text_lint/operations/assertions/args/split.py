"""String splits assertion operation YAML argument definitions."""

from typing import Any, Dict, List, Optional

from text_lint.exceptions.schema import SplitGroupInvalid

AliasYamlSplit = Optional[List[Dict[str, Any]]]


class SplitArgs:
  """String splits YAML argument definitions."""

  def __init__(self, splits: List["Split"]) -> None:
    self.splits = splits

  @classmethod
  def create(cls, yaml_input: Optional[AliasYamlSplit]) -> "SplitArgs":
    """Create an instance from YAML input."""

    created_splits = []
    if yaml_input is not None:
      for yaml_split in yaml_input:
        created_splits.append(Split(**yaml_split))
    return cls(splits=created_splits)

  def as_dict(self) -> Dict[int, Optional[str]]:
    """Return a dictionary representation of the splits."""

    return {split.group: split.separator for split in self.splits}


class Split:
  """String split definition."""

  def __init__(
      self,
      group: int,
      separator: Optional[str] = None,
  ) -> None:
    if group < 1:
      raise SplitGroupInvalid

    self.group = group
    self.separator = separator
