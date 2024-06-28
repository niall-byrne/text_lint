"""Test the StateFactory class."""

from unittest import mock

from .. import StateFactory
from ..assertion import AssertionState
from ..lookup import LookupState
from ..validator import ValidatorState


class TestStateFactory:
  """Test the StateFactory class."""

  def test_assertion__returns_correct_state(
      self,
      mocked_linter: mock.Mock,
  ) -> None:
    instance = StateFactory(linter=mocked_linter)

    result = instance.assertion()

    assert isinstance(result, AssertionState)
    # pylint: disable=protected-access
    assert result._linter == mocked_linter

  def test_lookup__returns_correct_state(
      self,
      mocked_linter: mock.Mock,
  ) -> None:
    instance = StateFactory(linter=mocked_linter)

    result = instance.lookup()

    assert isinstance(result, LookupState)
    # pylint: disable=protected-access
    assert result._linter == mocked_linter

  def test_validator__returns_correct_state(
      self,
      mocked_linter: mock.Mock,
  ) -> None:
    instance = StateFactory(linter=mocked_linter)

    result = instance.validator()

    assert isinstance(result, ValidatorState)
    # pylint: disable=protected-access
    assert result._linter == mocked_linter
