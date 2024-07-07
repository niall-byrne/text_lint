"""LoopPattern class."""

from typing import TYPE_CHECKING, Any

from .bases.pattern_base import SequencerPatternBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.sequencers.bases.sequencer_base import SequencerBase


class LinearPattern(SequencerPatternBase):
  """Linear pattern for SequencerBase instances."""

  def increment(self, sequencer: "SequencerBase[Any]") -> None:
    """Advance the index for the given sequencer instance."""

    if sequencer.index < len(sequencer):
      sequencer.index += 1
    else:
      raise StopIteration
