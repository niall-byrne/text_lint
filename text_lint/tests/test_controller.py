"""Test the Controller class."""

from typing import List
from unittest import mock

import pytest
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.sequencers import UnconsumedData
from ..controller import Controller


class TestController:
  """Test the Controller class."""

  def test_initialize__translations(
      self,
      controller_instance: Controller,
  ) -> None:
    assert_is_translated(controller_instance.msg_fmt_all_rules_not_read)
    assert_is_translated(controller_instance.msg_fmt_entire_file_not_read)

  # pylint: disable=unused-argument
  def test_initialize__creates_schema_instance(
      self,
      mocked_schema_path: str,
      mocked_schema: mock.Mock,
      controller_instance: Controller,
  ) -> None:
    mocked_schema.assert_called_once_with(mocked_schema_path)

  def test_initialize__creates_rules_sequencer_instance(
      self,
      mocked_rule_sequencer: mock.Mock,
      mocked_schema: mock.Mock,
      controller_instance: Controller,
  ) -> None:
    mocked_rule_sequencer.assert_called_once_with(mocked_schema.return_value)
    assert controller_instance.rules == mocked_rule_sequencer.return_value

  def test_initialize__creates_validator_sequencer_instance(
      self,
      mocked_schema: mock.Mock,
      mocked_validator_sequencer: mock.Mock,
      controller_instance: Controller,
  ) -> None:
    mocked_validator_sequencer.assert_called_once_with(
        mocked_schema.return_value
    )
    assert controller_instance.validators == (
        mocked_validator_sequencer.return_value
    )

  def test_initialize__creates_and_configures_text_file_sequencer_instance(
      self,
      mocked_file_path: str,
      mocked_text_file_sequencer: mock.Mock,
      mocked_schema: mock.Mock,
      controller_instance: Controller,
  ) -> None:
    mocked_text_file_sequencer.assert_called_once_with(mocked_file_path)
    mocked_text_file_sequencer.return_value.configure.\
        assert_called_once_with(mocked_schema.return_value)
    assert controller_instance.textfile == (
        mocked_text_file_sequencer.return_value
    )

  def test_initialize__creates_result_forest_instance(
      self,
      mocked_result_forest: mock.Mock,
      controller_instance: Controller,
  ) -> None:
    mocked_result_forest.assert_called_once_with()
    assert controller_instance.forest == mocked_result_forest.return_value

  def test_start__all_text__all_schema__rules_finish__run_all_rules(
      self,
      mocked_rule_sequencer: mock.MagicMock,
      mocked_sequence: List[mock.Mock],
      mocked_text_file_sequencer: mock.Mock,
      controller_instance: Controller,
  ) -> None:
    mocked_rule_sequencer.return_value.__iter__.return_value = mocked_sequence
    mocked_rule_sequencer.return_value.__next__.side_effect = StopIteration
    mocked_text_file_sequencer.return_value.__next__.side_effect = (
        StopIteration
    )

    controller_instance.start()

    for mocked_rule in mocked_sequence:
      mocked_rule.apply.assert_called_once_with(controller_instance)

  def test_start__all_text__all_schema__rules_finish__add_all_results(
      self,
      mocked_result_forest: mock.Mock,
      mocked_rule_sequencer: mock.MagicMock,
      mocked_sequence: List[mock.Mock],
      mocked_text_file_sequencer: mock.Mock,
      controller_instance: Controller,
  ) -> None:
    mocked_rule_sequencer.return_value.__iter__.return_value = mocked_sequence
    mocked_rule_sequencer.return_value.__next__.side_effect = StopIteration
    mocked_text_file_sequencer.return_value.__next__.side_effect = (
        StopIteration
    )

    controller_instance.start()

    mocked_results: List[mock.Mock] = []
    for mocked_rule in mocked_sequence:
      mocked_rule.apply.assert_called_once_with(controller_instance)
      mocked_results.append(mocked_rule.results)
    mocked_result_forest.return_value.add.assert_has_calls(
        [mock.call(result) for result in mocked_results]
    )

  def test_start__all_text__all_schema__rules_finish__run_all_validators(
      self,
      mocked_rule_sequencer: mock.MagicMock,
      mocked_sequence: List[mock.Mock],
      mocked_text_file_sequencer: mock.Mock,
      mocked_validator_sequencer: mock.MagicMock,
      controller_instance: Controller,
  ) -> None:
    mocked_rule_sequencer.return_value.__next__.side_effect = StopIteration
    mocked_text_file_sequencer.return_value.__next__.side_effect = (
        StopIteration
    )
    mocked_validator_sequencer.return_value.__iter__.return_value = (
        mocked_sequence
    )

    controller_instance.start()

    for mocked_validator in mocked_sequence:
      mocked_validator.apply.assert_called_once_with(controller_instance)

  def test_start__all_text__all_schema__rules_signal_stop__run_some_rules(
      self,
      mocked_rule_sequencer: mock.MagicMock,
      mocked_sequence: List[mock.Mock],
      mocked_text_file_sequencer: mock.Mock,
      controller_instance: Controller,
  ) -> None:
    mocked_rule_sequencer.return_value.__iter__.return_value = mocked_sequence
    mocked_rule_sequencer.return_value.__next__.side_effect = StopIteration
    mocked_text_file_sequencer.return_value.__next__.side_effect = (
        StopIteration
    )
    mocked_sequence[1].apply.side_effect = StopIteration

    controller_instance.start()

    mocked_sequence[0].apply.assert_called_once_with(controller_instance)
    mocked_sequence[1].apply.assert_called_once_with(controller_instance)
    mocked_sequence[2].apply.assert_not_called()

  def test_start__all_text__all_schema__rules_signal_stop__add_some_results(
      self,
      mocked_result_forest: mock.Mock,
      mocked_rule_sequencer: mock.MagicMock,
      mocked_sequence: List[mock.Mock],
      mocked_text_file_sequencer: mock.Mock,
      controller_instance: Controller,
  ) -> None:
    mocked_rule_sequencer.return_value.__iter__.return_value = mocked_sequence
    mocked_rule_sequencer.return_value.__next__.side_effect = StopIteration
    mocked_text_file_sequencer.return_value.__next__.side_effect = (
        StopIteration
    )
    mocked_sequence[1].apply.side_effect = StopIteration

    controller_instance.start()

    mocked_sequence[0].apply.assert_called_once_with(controller_instance)
    mocked_sequence[1].apply.assert_called_once_with(controller_instance)
    mocked_sequence[2].apply.assert_not_called()
    mocked_result_forest.return_value.add.assert_called_once_with(
        mocked_sequence[0].results
    )

  def test_start__all_text__all_schema__rules_signal_stop__run_all_validators(
      self,
      mocked_rule_sequencer: mock.MagicMock,
      mocked_sequence: List[mock.Mock],
      mocked_text_file_sequencer: mock.Mock,
      mocked_validator_sequencer: mock.MagicMock,
      controller_instance: Controller,
  ) -> None:
    mocked_rule_with_stop_signal = mock.Mock()
    mocked_rule_with_stop_signal.apply.side_effect = StopIteration
    mocked_rule_sequencer.return_value.__iter__.return_value = [
        mocked_rule_with_stop_signal
    ]
    mocked_rule_sequencer.return_value.__next__.side_effect = StopIteration
    mocked_text_file_sequencer.return_value.__next__.side_effect = (
        StopIteration
    )
    mocked_validator_sequencer.return_value.__iter__.return_value = (
        mocked_sequence
    )

    controller_instance.start()

    for mocked_validator in mocked_sequence:
      mocked_validator.apply.assert_called_once_with(controller_instance)

  def test_start__all_text__partial_schema__run_some_rules__raise_exception(
      self,
      mocked_rule_sequencer: mock.MagicMock,
      mocked_sequence: List[mock.Mock],
      mocked_text_file_sequencer: mock.Mock,
      controller_instance: Controller,
  ) -> None:
    mocked_rule_sequencer.return_value.__iter__.return_value = mocked_sequence
    mocked_text_file_sequencer.return_value.__next__.side_effect = (
        StopIteration
    )

    with pytest.raises(UnconsumedData) as exc:
      controller_instance.start()

    for mocked_rule in mocked_sequence:
      mocked_rule.apply.assert_called_once_with(controller_instance)
      assert str(exc.value) == controller_instance.msg_fmt_all_rules_not_read

  def test_start__all_text__partial_schema__run_no_validators__raise_exception(
      self,
      mocked_sequence: List[mock.Mock],
      mocked_validator_sequencer: mock.MagicMock,
      controller_instance: Controller,
      translations: mock.Mock,
  ) -> None:
    mocked_validator_sequencer.return_value.__iter__.return_value = (
        mocked_sequence
    )

    with pytest.raises(UnconsumedData) as exc:
      controller_instance.start()

    for mocked_validator in mocked_sequence:
      mocked_validator.apply.assert_not_called()

    assert str(exc.value) == controller_instance.msg_fmt_all_rules_not_read

  def test_start__partial_text__all_schema__run_all_rules__raise_exception(
      self,
      mocked_rule_sequencer: mock.MagicMock,
      mocked_sequence: List[mock.Mock],
      mocked_text_file_sequencer: mock.Mock,
      controller_instance: Controller,
  ) -> None:
    mocked_rule_sequencer.return_value.__iter__.return_value = mocked_sequence
    mocked_rule_sequencer.return_value.__next__.side_effect = StopIteration

    with pytest.raises(UnconsumedData) as exc:
      controller_instance.start()

    for mocked_rule in mocked_sequence:
      mocked_rule.apply.assert_called_once_with(controller_instance)
    assert str(exc.value) == controller_instance.msg_fmt_entire_file_not_read

  def test_start__partial_text__all_schema__run_no_validators__raise_exception(
      self,
      mocked_rule_sequencer: mock.MagicMock,
      mocked_sequence: List[mock.Mock],
      mocked_validator_sequencer: mock.MagicMock,
      controller_instance: Controller,
      translations: mock.Mock,
  ) -> None:
    mocked_rule_sequencer.return_value.__next__.side_effect = StopIteration
    mocked_validator_sequencer.return_value.__iter__.return_value = (
        mocked_sequence
    )

    with pytest.raises(UnconsumedData) as exc:
      controller_instance.start()

    for mocked_validator in mocked_sequence:
      mocked_validator.apply.assert_not_called()
    assert str(exc.value) == controller_instance.msg_fmt_entire_file_not_read
