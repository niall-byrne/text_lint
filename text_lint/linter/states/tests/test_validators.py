"""Test the ValidatorState class."""

from unittest import mock

from ..bases.state_base import StateBase
from ..validator import ValidatorState


class TestValidatorState:
  """Test the ValidatorState class."""

  def test_initialize__attributes(
      self,
      validator_state_instance: ValidatorState,
      mocked_linter: mock.Mock,
  ) -> None:
    # pylint: disable=protected-access
    assert validator_state_instance._linter == mocked_linter
    assert validator_state_instance.operation == mocked_linter.validators.last

  def test_initialize__inheritance(
      self,
      validator_state_instance: ValidatorState,
  ) -> None:
    assert isinstance(
        validator_state_instance,
        ValidatorState,
    )
    assert isinstance(
        validator_state_instance,
        StateBase,
    )

  def test_lookup_expression__calls_linter_methods(
      self,
      validator_state_instance: ValidatorState,
      mocked_linter: mock.Mock,
  ) -> None:
    mocked_lookup_expression = mock.Mock()

    validator_state_instance.lookup_expression(
        lookup_expression=mocked_lookup_expression
    )

    mocked_linter.forest.lookup_expression.assert_called_once_with(
        mocked_linter,
        mocked_lookup_expression,
    )
