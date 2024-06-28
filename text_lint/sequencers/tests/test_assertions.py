"""Test AssertionSequencer class."""

from typing import Type
from unittest import mock

from text_lint.sequencers.assertions import AssertionSequencer
from text_lint.sequencers.bases.operator_base import OperatorBase
from text_lint.sequencers.bases.sequencer_base import SequencerBase


class TestAssertionSequencer:
  """Test the AssertionSequencer class."""

  def test_initialize__attributes(
      self,
      assertions_sequencer_class: Type[AssertionSequencer],
      mocked_schema: mock.Mock,
  ) -> None:
    instance = assertions_sequencer_class(mocked_schema)

    assert instance.index == 0

  def test_initialize__loads_assertions_from_schema(
      self,
      assertions_sequencer_class: Type[AssertionSequencer],
      mocked_schema: mock.Mock,
  ) -> None:
    assertions_sequencer_class(mocked_schema)

    mocked_schema.load_assertions.assert_called_once_with()

  def test_initialize__inheritance(
      self,
      assertions_sequencer_class: Type[AssertionSequencer],
      mocked_schema: mock.Mock,
  ) -> None:
    instance = assertions_sequencer_class(mocked_schema)

    assert isinstance(instance, AssertionSequencer)
    assert isinstance(instance, OperatorBase)
    assert isinstance(instance, SequencerBase)

  def test_next__iterates_over_schema_content(
      self,
      assertions_sequencer_class: Type[AssertionSequencer],
      mocked_schema: mock.Mock,
  ) -> None:
    mocked_schema.load_assertions.return_value = ["one", "two", "three"]
    instance = assertions_sequencer_class(mocked_schema)

    received_operations = list(instance)

    assert received_operations == mocked_schema.load_assertions.return_value
