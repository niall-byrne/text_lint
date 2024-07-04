"""Exceptions for the text_lint sequencers."""


class SequencerExceptionBase(Exception):
  """Base class for sequencer exceptions."""


class UnconsumedData(Exception):
  """Raised when a sequencer unexpectedly has remaining data."""
