"""LoopPattern class."""


class LoopPattern:
  """Loop pattern for OperatorBase instances."""

  def __init__(
      self,
      start: int,
      end: int,
  ) -> None:
    self.start = start
    self.end = end
