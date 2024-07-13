"""Test the ValidatorState class."""

from unittest import mock

import pytest
from text_lint.__helpers__.validators import assert_is_validation_failure
from text_lint.exceptions.validators import ValidationFailure
from text_lint.utilities.translations import _
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

  def test_fail__raises_exception(
      self,
      validator_state_instance: ValidatorState,
  ) -> None:
    mocked_translated_description = _("mocked_translated_description")
    mocked_translated_detail = _("mocked_translated_detail")

    with pytest.raises(ValidationFailure) as exc:
      validator_state_instance.fail(
          translated_description=mocked_translated_description,
          translated_detail=mocked_translated_detail
      )

    assert_is_validation_failure(
        exc=exc,
        description_t=(mocked_translated_description,),
        detail_t=(mocked_translated_detail,),
        validator=validator_state_instance.operation,
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

  def test_save__calls_linter_methods(
      self,
      validator_state_instance: ValidatorState,
      mocked_linter: mock.Mock,
  ) -> None:
    mocked_result_tree = mock.Mock()

    validator_state_instance.save(mocked_result_tree)

    mocked_linter.forest.add.assert_called_once_with(mocked_result_tree)
