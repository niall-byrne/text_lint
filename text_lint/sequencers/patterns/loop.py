"""LinearLoopPattern class."""

from typing import TYPE_CHECKING, Any

from .linear import LinearPattern

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.sequencers.bases.sequencer_base import SequencerBase


class LinearLoopPattern(LinearPattern):
  """Linear loop pattern for SequencerBase instances."""

  def __init__(
      self,
      start: int,
      end: int,
  ) -> None:
    self.start = start
    self.end = end

  def adjust(self, offset: int) -> None:
    """Adjust the pattern based on inserted data."""

    self.end += offset

  def increment(self, sequencer: "SequencerBase[Any]") -> None:
    """Advance the index for the given sequencer instance."""

    if sequencer.index + 1 >= self.end:
      sequencer.index = self.start
    else:
      super().increment(sequencer)
