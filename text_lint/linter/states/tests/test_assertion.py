"""Test the AssertionState class."""

import re
from typing import TYPE_CHECKING, List, Match
from unittest import mock

import pytest
from text_lint.__helpers__.assertion import (
    assert_is_assertion_logic_error,
    assert_is_assertion_violation,
)
from text_lint.exceptions.assertions import (
    AssertionLogicError,
    AssertionViolation,
)
from ..assertion import AssertionState
from ..bases.state_base import StateBase

if TYPE_CHECKING:  # no cover
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )


class TestAssertionState:
  """Test the AssertionState class."""

  def test_initialize__attributes(
      self,
      assertion_state_instance: AssertionState,
      mocked_linter: mock.Mock,
  ) -> None:
    # pylint: disable=protected-access
    assert assertion_state_instance._linter == mocked_linter
    assert assertion_state_instance.rewound == -1
    assert assertion_state_instance.operation == mocked_linter.assertions.last

  def test_initialize__inheritance(
      self,
      assertion_state_instance: AssertionState,
  ) -> None:
    assert isinstance(
        assertion_state_instance,
        AssertionState,
    )
    assert isinstance(
        assertion_state_instance,
        StateBase,
    )

  def test_loop__calls_linter_methods(
      self,
      assertion_state_instance: AssertionState,
      mocked_assertions: List["AssertionBase"],
      mocked_linter: mock.Mock,
  ) -> None:
    mocked_count = -1

    assertion_state_instance.loop(
        assertions=mocked_assertions,
        count=mocked_count,
    )

    mocked_linter.assertions.start_repeating.assert_called_once_with(
        mocked_count
    )
    mocked_linter.assertions.insert.assert_called_once_with(mocked_assertions)

  def test_loop_stop__calls_linter_methods(
      self,
      assertion_state_instance: AssertionState,
      mocked_linter: mock.Mock,
  ) -> None:
    assertion_state_instance.loop_stop()

    mocked_linter.assertions.stop_repeating.assert_called_once_with()

  def test_next__calls_linter_methods(
      self,
      assertion_state_instance: AssertionState,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_file_line = "mocked_file_line"
    mocked_textfile.__next__.return_value = mocked_file_line

    result = assertion_state_instance.next()

    mocked_textfile.__next__.assert_called_once_with()
    assert result == mocked_file_line

  def test_rewind__called_once__updates_text_file_index(
      self,
      assertion_state_instance: AssertionState,
      mocked_linter: mock.Mock,
  ) -> None:
    mocked_linter.textfile.index = 100

    assertion_state_instance.rewind()

    assert mocked_linter.textfile.index == 99

  def test_rewind__called_twice_on_different_lines__updates_text_file_index(
      self,
      assertion_state_instance: AssertionState,
      mocked_linter: mock.Mock,
  ) -> None:
    mocked_linter.textfile.index = 100

    assertion_state_instance.rewind()
    mocked_linter.textfile.index += 1
    assertion_state_instance.rewind()

    assert mocked_linter.textfile.index == 99

  def test_rewind__called_twice_on_same_line__raises_exception(
      self,
      assertion_state_instance: AssertionState,
      mocked_linter: mock.Mock,
  ) -> None:
    mocked_linter.textfile.index = 100

    with pytest.raises(AssertionLogicError) as exc:
      assertion_state_instance.rewind()
      assertion_state_instance.rewind()

    assert_is_assertion_logic_error(
        exc=exc,
        assertion=mocked_linter.assertions.last,
        textfile=mocked_linter.textfile,
        hint=assertion_state_instance.msg_fmt_logic_error_rewind,
    )

  @pytest.mark.parametrize("matches", [re.match("one", "two"), []])
  def test_save__called_with_no_matches__does_not_call_linter_method(
      self,
      assertion_state_instance: AssertionState,
      mocked_linter: mock.Mock,
      matches: List[Match[str]],
  ) -> None:
    assertion_state_instance.save(matches)

    mocked_linter.forest.add.assert_not_called()

  @pytest.mark.parametrize("match", [re.match("one", "one")])
  def test_save__called_with_single_match__calls_linter_method(
      self,
      assertion_state_instance: AssertionState,
      mocked_linter: mock.Mock,
      match: Match[str],
  ) -> None:
    created_tree = mocked_linter.assertions.last.create_result_tree.return_value

    assertion_state_instance.save(match)

    mocked_linter.assertions.last.create_result_tree.assert_called_once_with(
        [match]
    )
    mocked_linter.forest.add.assert_called_once_with(created_tree)

  @pytest.mark.parametrize(
      "matches", [[re.match("one", "one"), [re.match("two", "two")]]]
  )
  def test_save__called_with_multiple_matches__calls_linter_method(
      self,
      assertion_state_instance: AssertionState,
      mocked_linter: mock.Mock,
      matches: List[Match[str]],
  ) -> None:
    created_tree = mocked_linter.assertions.last.create_result_tree.return_value

    assertion_state_instance.save(matches)

    mocked_linter.assertions.last.create_result_tree.assert_called_once_with(
        matches
    )
    mocked_linter.forest.add.assert_called_once_with(created_tree)

  def test_fail__called_with_expected_text__raises_exception(
      self,
      assertion_state_instance: AssertionState,
      mocked_linter: mock.Mock,
  ) -> None:
    mocked_expected_text = "mocked_expected_text"

    with pytest.raises(AssertionViolation) as exc:
      assertion_state_instance.fail(mocked_expected_text)

    assert_is_assertion_violation(
        exc=exc,
        assertion=mocked_linter.assertions.last,
        textfile=mocked_linter.textfile,
        expected=mocked_expected_text,
    )
