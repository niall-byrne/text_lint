"""Sequencer pattern base class."""

import abc
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.sequencers.bases.operator_base import SequencerBase


class SequencerPatternBase(abc.ABC):
  """Base pattern for incrementing sequencer instances."""

  # pylint: disable=unused-argument
  def adjust(self, offset: int) -> None:
    """Adjust the pattern based on inserted data.

    :param offset: An index to adjust the pattern by.
    """

  @abc.abstractmethod
  def increment(self, sequencer: "SequencerBase[Any]") -> None:
    """Advance the index for the given sequencer instance.

    :param sequencer: The sequencer instance to advance.
    """
