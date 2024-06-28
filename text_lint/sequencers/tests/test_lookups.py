"""Test LookupsSequencer class."""

from typing import Dict, Type
from unittest import mock

from text_lint.sequencers.bases.operator_base import OperatorBase
from text_lint.sequencers.bases.sequencer_base import SequencerBase
from text_lint.sequencers.lookups import LookupsSequencer


class TestLookupsSequencer:
  """Test the LookupsSequencer class."""

  def test_initialize__attributes(
      self,
      lookups_sequencer_class: Type[LookupsSequencer],
      mocked_result_set: mock.Mock,
  ) -> None:
    instance = lookups_sequencer_class(
        mocked_result_set,
        "mocked_requesting_operation_name",
    )

    assert instance.index == 0

  def test_initialize__inheritance(
      self,
      lookups_sequencer_class: Type[LookupsSequencer],
      mocked_result_set: mock.Mock,
  ) -> None:
    instance = lookups_sequencer_class(
        mocked_result_set,
        "mocked_requesting_operation_name",
    )

    assert isinstance(instance, LookupsSequencer)
    assert isinstance(instance, OperatorBase)
    assert isinstance(instance, SequencerBase)

  def test_initialize__creates_correct_lookup_instances(
      self,
      lookups_sequencer_class: Type[LookupsSequencer],
      mocked_lookup_registry: Dict[str, mock.Mock],
      mocked_result_set: mock.Mock,
  ) -> None:
    _ = lookups_sequencer_class(
        mocked_result_set,
        "mocked_requesting_operation_name",
    )

    for lookup in mocked_lookup_registry.keys():
      mocked_lookup_registry[lookup].assert_called_once_with(
          lookup,
          mocked_result_set,
          "mocked_requesting_operation_name",
      )

  def test_next__iterates_over_correct_lookup_instances(
      self,
      lookups_sequencer_class: Type[LookupsSequencer],
      mocked_lookup_registry: Dict[str, mock.Mock],
      mocked_result_set: mock.Mock,
  ) -> None:
    instance = lookups_sequencer_class(
        mocked_result_set,
        "mocked_requesting_operation_name",
    )

    received_operations = list(instance)

    assert received_operations == [
        mocked_lookup_registry[lookup].return_value
        for lookup in mocked_lookup_registry.keys()
    ]
