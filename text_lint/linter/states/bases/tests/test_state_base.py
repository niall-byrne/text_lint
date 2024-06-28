"""Test the StateBase class."""

from unittest import mock

import pytest
from ..state_base import StateBase


class TestStateBase:
  """Test the StateBase class."""

  def test_initialize__attributes(
      self,
      concrete_state_base_instance: StateBase,
      mocked_linter: mock.Mock,
  ) -> None:
    # pylint: disable=protected-access
    assert concrete_state_base_instance._linter == mocked_linter

  @pytest.mark.parametrize("indent", [True, False])
  def test_log__calls_linter_logger(
      self,
      concrete_state_base_instance: StateBase,
      mocked_linter: mock.Mock,
      indent: bool,
  ) -> None:
    mocked_message = "mocked_message"

    concrete_state_base_instance.log(
        mocked_message,
        indent=indent,
    )

    mocked_linter.log.assert_called_once_with(
        mocked_message,
        indent=indent,
    )
