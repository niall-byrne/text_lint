"""Test the Linter class."""

from typing import List
from unittest import mock

import pytest
from text_lint import linter
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.sequencers import UnconsumedData
from text_lint.linter import Linter
from text_lint.linter.settings import LinterSettings
from text_lint.sequencers.patterns.loop import LinearLoopPattern


class TestLinter:
  """Test the Linter class."""

  def test_initialize__translations(
      self,
      linter_instance: Linter,
  ) -> None:
    assert_is_translated(linter_instance.msg_fmt_all_assertions_not_read)
    assert_is_translated(linter_instance.msg_fmt_entire_file_not_read)

  def test_initialize__creates_settings_instance(
      self,
      mocked_file_path: str,
      mocked_schema_path: str,
      linter_instance: Linter,
  ) -> None:
    assert isinstance(linter_instance.settings, LinterSettings)
    assert linter_instance.settings.file_path == mocked_file_path
    assert linter_instance.settings.schema_path == mocked_schema_path

  @pytest.mark.parametrize("interpolate", [True, False])
  @pytest.mark.usefixtures("setup_linter_mocks")
  def test_initialize__creates_schema_instance(
      self,
      mocked_file_path: str,
      mocked_schema_path: str,
      mocked_schema: mock.Mock,
      interpolate: bool,
  ) -> None:
    settings = LinterSettings(
        file_path=mocked_file_path,
        interpolate_schema=interpolate,
        quiet=False,
        schema_path=mocked_schema_path,
    )

    Linter(settings=settings)

    mocked_schema.assert_called_once_with(mocked_schema_path, interpolate)

  def test_initialize__creates_assertions_sequencer_instance(
      self,
      mocked_sequencer_assertions: mock.Mock,
      mocked_schema: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    mocked_sequencer_assertions.assert_called_once_with(
        mocked_schema.return_value
    )
    assert linter_instance.assertions == (
        mocked_sequencer_assertions.return_value
    )

  def test_initialize__creates_validator_sequencer_instance(
      self,
      mocked_schema: mock.Mock,
      mocked_sequencer_validators: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    mocked_sequencer_validators.assert_called_once_with(
        mocked_schema.return_value
    )
    assert linter_instance.validators == (
        mocked_sequencer_validators.return_value
    )

  def test_initialize__creates_state_factory_instance(
      self,
      mocked_state_factory: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    mocked_state_factory.assert_called_once_with(linter_instance)
    assert linter_instance.states == mocked_state_factory.return_value

  def test_initialize__creates_and_configures_text_file_sequencer_instance(
      self,
      mocked_file_path: str,
      mocked_sequencer_text_file: mock.Mock,
      mocked_schema: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    mocked_sequencer_text_file.assert_called_once_with(mocked_file_path)
    mocked_sequencer_text_file.return_value.configure.\
        assert_called_once_with(mocked_schema.return_value)
    assert linter_instance.textfile == mocked_sequencer_text_file.return_value

  def test_initialize__creates_recursion_detection_instance(
      self,
      mocked_recursion_detection: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    mocked_recursion_detection.assert_called_once_with(linter_instance)
    assert linter_instance.recursion == (
        mocked_recursion_detection.return_value
    )

  def test_initialize__creates_result_forest_instance(
      self,
      mocked_result_forest: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    mocked_result_forest.assert_called_once_with()
    assert linter_instance.forest == mocked_result_forest.return_value

  def test_initialize__creates_logger(
      self,
      mocked_logger: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    mocked_logger.assert_called_once_with(linter_instance)
    assert linter_instance.log == mocked_logger.return_value

  @pytest.mark.usefixtures("scenario__all_text__all_schema__all_assertions")
  def test_start__all_text__all_schema__assertions_finish__logs_correctly(
      self,
      linter_instance: Linter,
      mocked_sequence_assertions: List[mock.Mock],
      mocked_sequence_validators: List[mock.Mock],
      monkeypatch: pytest.MonkeyPatch,
  ) -> None:
    logging_contexts_mock = mock.MagicMock(unsafe=True)
    monkeypatch.setattr(
        linter,
        "logging_contexts",
        logging_contexts_mock,
    )

    linter_instance.start()

    # pylint: disable=unnecessary-dunder-call
    assert logging_contexts_mock.mock_calls == [
        mock.call.main(linter_instance),
        mock.call.main().__enter__(),
        mock.call.assertion_section(linter_instance),
        mock.call.assertion_section().__enter__(),
    ] + [
        call for nested_calls in [
            [
                mock.call.assertion(linter_instance, assertion),
                mock.call.assertion().__enter__(),
                mock.call.assertion().__exit__(None, None, None)
            ] for assertion in mocked_sequence_assertions
        ] for call in nested_calls
    ] + [
        mock.call.assertion_section().__exit__(None, None, None),
        mock.call.validator_section(linter_instance),
        mock.call.validator_section().__enter__(),
    ] + [
        call for nested_calls in [
            [
                mock.call.validator(linter_instance, validator),
                mock.call.validator().__enter__(),
                mock.call.validator().__exit__(None, None, None)
            ] for validator in mocked_sequence_validators
        ] for call in nested_calls
    ] + [
        mock.call.validator_section().__exit__(None, None, None),
        mock.call.main().__exit__(None, None, None),
    ]

  @pytest.mark.usefixtures("scenario__all_text__all_schema__all_assertions")
  def test_start__all_text__all_schema__assertions_finish__run_all_assertions(
      self,
      mocked_sequence_assertions: List[mock.Mock],
      mocked_state_factory: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    linter_instance.start()

    for mocked_assertion in mocked_sequence_assertions:
      mocked_assertion.apply.assert_called_once_with(
          mocked_state_factory.return_value.assertion.return_value
      )
    assert mocked_state_factory.return_value.assertion.mock_calls == (
        [mock.call()] * len(mocked_sequence_assertions)
    )

  @pytest.mark.usefixtures("scenario__all_text__all_schema__all_assertions")
  def test_start__all_text__all_schema__assertions_finish__detect_recursion(
      self,
      mocked_recursion_detection: mock.Mock,
      mocked_sequence_assertions: List[mock.Mock],
      linter_instance: Linter,
  ) -> None:
    recursion_instance = mocked_recursion_detection.return_value

    linter_instance.start()

    assert recursion_instance.detect.mock_calls == (
        [mock.call()] * len(mocked_sequence_assertions)
    )

  @pytest.mark.usefixtures("scenario__all_text__all_schema__all_assertions")
  def test_start__all_text__all_schema__assertions_finish__run_all_validators(
      self,
      mocked_sequence_validators: List[mock.Mock],
      mocked_state_factory: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    linter_instance.start()

    for mocked_validator in mocked_sequence_validators:
      mocked_validator.apply.assert_called_once_with(
          mocked_state_factory.return_value.validator.return_value
      )
    assert mocked_state_factory.return_value.validator.mock_calls == (
        [mock.call()] * len(mocked_sequence_validators)
    )

  @pytest.mark.usefixtures("scenario__all_text__all_schema__some_assertions")
  def test_start__all_text__all_schema__assertions_stop__run_some_assertions(
      self,
      mocked_sequence_assertions: List[mock.Mock],
      mocked_state_factory: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    linter_instance.start()

    mocked_sequence_assertions[0].apply.assert_called_once_with(
        mocked_state_factory.return_value.assertion.return_value
    )
    mocked_sequence_assertions[1].apply.assert_called_once_with(
        mocked_state_factory.return_value.assertion.return_value
    )
    mocked_sequence_assertions[2].apply.assert_not_called()
    assert mocked_state_factory.return_value.assertion.mock_calls == (
        [mock.call()] * (len(mocked_sequence_assertions) - 1)
    )

  @pytest.mark.usefixtures("scenario__all_text__all_schema__some_assertions")
  def test_start__all_text__all_schema__assertions_stop__detect_recursion(
      self,
      mocked_recursion_detection: mock.Mock,
      mocked_sequence_assertions: List[mock.Mock],
      linter_instance: Linter,
  ) -> None:
    recursion_instance = mocked_recursion_detection.return_value

    linter_instance.start()

    assert recursion_instance.detect.mock_calls == (
        [mock.call()] * (len(mocked_sequence_assertions) - 2)
    )

  @pytest.mark.usefixtures("scenario__all_text__all_schema__some_assertions")
  def test_start__all_text__all_schema__assertions_stop__run_all_validators(
      self,
      mocked_sequence_validators: List[mock.Mock],
      mocked_state_factory: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    linter_instance.start()

    for mocked_validator in mocked_sequence_validators:
      mocked_validator.apply.assert_called_once_with(
          mocked_state_factory.return_value.validator.return_value
      )
    assert mocked_state_factory.return_value.validator.mock_calls == (
        [mock.call()] * len(mocked_sequence_validators)
    )

  @pytest.mark.usefixtures("scenario__all_text__all_schema__some_assertions")
  def test_start__all_text__all_schema__loop_signals_stop__run_assertions(
      self,
      mocked_sequence_assertions: List[mock.Mock],
      mocked_state_factory: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    linter_instance.assertions.pattern = mock.Mock(spec=LinearLoopPattern)

    linter_instance.start()

    mocked_sequence_assertions[0].apply.assert_called_once_with(
        mocked_state_factory.return_value.assertion.return_value
    )
    mocked_sequence_assertions[1].apply.assert_called_once_with(
        mocked_state_factory.return_value.assertion.return_value
    )
    mocked_sequence_assertions[2].apply.assert_not_called()
    assert mocked_state_factory.return_value.assertion.mock_calls == (
        [mock.call()] * (len(mocked_sequence_assertions) - 1)
    )

  @pytest.mark.usefixtures("scenario__all_text__all_schema__some_assertions")
  def test_start__all_text__all_schema__loop_signals_stop__detect_recursion(
      self,
      mocked_recursion_detection: mock.Mock,
      mocked_sequence_assertions: List[mock.Mock],
      linter_instance: Linter,
  ) -> None:
    linter_instance.assertions.pattern = mock.Mock(spec=LinearLoopPattern)
    recursion_instance = mocked_recursion_detection.return_value

    linter_instance.start()

    assert recursion_instance.detect.mock_calls == (
        [mock.call()] * (len(mocked_sequence_assertions) - 2)
    )

  @pytest.mark.usefixtures("scenario__all_text__all_schema__some_assertions")
  def test_start__all_text__all_schema__loop_signals_stop__run_all_validators(
      self,
      mocked_sequence_validators: List[mock.Mock],
      mocked_state_factory: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    linter_instance.assertions.pattern = mock.Mock(spec=LinearLoopPattern)

    linter_instance.start()

    for mocked_validator in mocked_sequence_validators:
      mocked_validator.apply.assert_called_once_with(
          mocked_state_factory.return_value.validator.return_value
      )
    assert mocked_state_factory.return_value.validator.mock_calls == (
        [mock.call()] * len(mocked_sequence_validators)
    )

  @pytest.mark.usefixtures("scenario__all_text__some_schema__all_assertions")
  def test_start__all_text__some_schema__loop_signals_stop__run_assertions(
      self,
      mocked_sequence_assertions: List[mock.Mock],
      mocked_state_factory: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    linter_instance.assertions.pattern = mock.Mock(spec=LinearLoopPattern)

    linter_instance.start()

    for mocked_assertion in mocked_sequence_assertions:
      mocked_assertion.apply.assert_called_once_with(
          mocked_state_factory.return_value.assertion.return_value
      )
    assert mocked_state_factory.return_value.assertion.mock_calls == (
        [mock.call()] * len(mocked_sequence_assertions)
    )

  @pytest.mark.usefixtures("scenario__all_text__some_schema__all_assertions")
  def test_start__all_text__some_schema__loop_signals_stop__detect_recursion(
      self,
      mocked_recursion_detection: mock.Mock,
      mocked_sequence_assertions: List[mock.Mock],
      linter_instance: Linter,
  ) -> None:
    linter_instance.assertions.pattern = mock.Mock(spec=LinearLoopPattern)
    recursion_instance = mocked_recursion_detection.return_value

    linter_instance.start()

    assert recursion_instance.detect.mock_calls == (
        [mock.call()] * len(mocked_sequence_assertions)
    )

  @pytest.mark.usefixtures("scenario__all_text__some_schema__all_assertions")
  def test_start__all_text__some_schema__loop_signals_stop__run_all_validators(
      self,
      mocked_sequence_validators: List[mock.Mock],
      mocked_state_factory: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    linter_instance.assertions.pattern = mock.Mock(spec=LinearLoopPattern)

    linter_instance.start()

    for mocked_validator in mocked_sequence_validators:
      mocked_validator.apply.assert_called_once_with(
          mocked_state_factory.return_value.validator.return_value
      )
    assert mocked_state_factory.return_value.validator.mock_calls == (
        [mock.call()] * len(mocked_sequence_validators)
    )

  @pytest.mark.usefixtures("scenario__all_text__some_schema__all_assertions")
  def test_start__all_text__some_schema__assertions_finish__raise_exception(
      self,
      mocked_recursion_detection: mock.Mock,
      mocked_sequence_assertions: List[mock.Mock],
      mocked_sequence_validators: List[mock.Mock],
      mocked_state_factory: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    recursion_instance = mocked_recursion_detection.return_value

    with pytest.raises(UnconsumedData) as exc:
      linter_instance.start()

    for index, mocked_assertion in enumerate(mocked_sequence_assertions):
      mocked_assertion.apply.assert_called_once_with(
          mocked_state_factory.return_value.assertion.return_value
      )
      assert recursion_instance.detect.mock_calls[index] == mock.call()
    for mocked_validator in mocked_sequence_validators:
      mocked_validator.apply.assert_not_called()
    assert str(exc.value) == \
           linter_instance.msg_fmt_all_assertions_not_read

  @pytest.mark.usefixtures("scenario__some_text__all_schema__all_assertions")
  def test_start__some_text__all_schema__assertions_finish__raise_exception(
      self,
      mocked_recursion_detection: mock.Mock,
      mocked_sequence_assertions: List[mock.Mock],
      mocked_sequence_validators: List[mock.Mock],
      mocked_state_factory: mock.Mock,
      linter_instance: Linter,
  ) -> None:
    recursion_instance = mocked_recursion_detection.return_value

    with pytest.raises(UnconsumedData) as exc:
      linter_instance.start()

    for index, mocked_assertion in enumerate(mocked_sequence_assertions):
      mocked_assertion.apply.assert_called_once_with(
          mocked_state_factory.return_value.assertion.return_value
      )
      assert recursion_instance.detect.mock_calls[index] == mock.call()
    for mocked_validator in mocked_sequence_validators:
      mocked_validator.apply.assert_not_called()
    assert str(exc.value) == linter_instance.msg_fmt_entire_file_not_read
