"""LoopPattern class."""


class LoopPattern:
  """Loop pattern for OperatorBase instances."""

  def __init__(
      self,
      index: int,
      count: int,
  ) -> None:
    self.index = index
    self.count = count
