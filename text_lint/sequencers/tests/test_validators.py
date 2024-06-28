"""Test ValidatorSequencer class."""

from typing import Type
from unittest import mock

from text_lint.sequencers.bases.operator_base import OperatorBase
from text_lint.sequencers.bases.sequencer_base import SequencerBase
from text_lint.sequencers.validators import ValidatorSequencer


class TestValidatorSequencer:
  """Test the ValidatorSequencer class."""

  def test_initialize__attributes(
      self, validator_sequencer_class: Type[ValidatorSequencer],
      mocked_schema: mock.Mock
  ) -> None:
    instance = validator_sequencer_class(mocked_schema)

    assert instance.index == 0

  def test_initialize__loads_rules_from_schema(
      self, validator_sequencer_class: Type[ValidatorSequencer],
      mocked_schema: mock.Mock
  ) -> None:
    validator_sequencer_class(mocked_schema)

    mocked_schema.load_validators()

  def test_initialize__inheritance(
      self, validator_sequencer_class: Type[ValidatorSequencer],
      mocked_schema: mock.Mock
  ) -> None:
    instance = validator_sequencer_class(mocked_schema)

    assert isinstance(instance, ValidatorSequencer)
    assert isinstance(instance, OperatorBase)
    assert isinstance(instance, SequencerBase)

  def test_next__iterates_over_schema_content(
      self, validator_sequencer_class: Type[ValidatorSequencer],
      mocked_schema: mock.Mock
  ) -> None:
    mocked_schema.load_validators.return_value = ["one", "two", "three"]
    instance = validator_sequencer_class(mocked_schema)

    received_operations = list(instance)

    assert received_operations == mocked_schema.load_validators.return_value
