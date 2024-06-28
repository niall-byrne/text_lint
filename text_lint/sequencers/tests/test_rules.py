"""Test RuleSequencer class."""

from typing import Type
from unittest import mock

from text_lint.sequencers.bases.operator_base import OperatorBase
from text_lint.sequencers.bases.sequencer_base import SequencerBase
from text_lint.sequencers.rules import RuleSequencer


class TestRuleSequencer:
  """Test the RuleSequencer class."""

  def test_initialize__attributes(
      self,
      rule_sequencer_class: Type[RuleSequencer],
      mocked_schema: mock.Mock,
  ) -> None:
    instance = rule_sequencer_class(mocked_schema)

    assert instance.index == 0

  def test_initialize__loads_rules_from_schema(
      self,
      rule_sequencer_class: Type[RuleSequencer],
      mocked_schema: mock.Mock,
  ) -> None:
    rule_sequencer_class(mocked_schema)

    mocked_schema.load_rules()

  def test_initialize__inheritance(
      self,
      rule_sequencer_class: Type[RuleSequencer],
      mocked_schema: mock.Mock,
  ) -> None:
    instance = rule_sequencer_class(mocked_schema)

    assert isinstance(instance, RuleSequencer)
    assert isinstance(instance, OperatorBase)
    assert isinstance(instance, SequencerBase)

  def test_next__iterates_over_schema_content(
      self,
      rule_sequencer_class: Type[RuleSequencer],
      mocked_schema: mock.Mock,
  ) -> None:
    mocked_schema.load_rules.return_value = ["one", "two", "three"]
    instance = rule_sequencer_class(mocked_schema)

    received_operations = list(instance)

    assert received_operations == mocked_schema.load_rules.return_value
