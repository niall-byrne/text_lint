"""Test the LookupState class."""

from unittest import mock

import pytest
from text_lint.__helpers__.lookups import assert_is_lookup_failure
from text_lint.exceptions.lookups import LookupFailure
from text_lint.utilities.translations import _
from ..bases.state_base import StateBase
from ..lookup import LookupState


class TestLookupState:
  """Test the LookupState class."""

  def test_initialize__attributes(
      self,
      lookup_state_instance: LookupState,
      mocked_linter: mock.Mock,
  ) -> None:
    # pylint: disable=protected-access
    assert lookup_state_instance._linter == mocked_linter

  def test_initialize__inheritance(
      self,
      lookup_state_instance: LookupState,
  ) -> None:
    assert isinstance(
        lookup_state_instance,
        LookupState,
    )
    assert isinstance(
        lookup_state_instance,
        StateBase,
    )

  def test_cursor__getter__retrieves_linter_values(
      self,
      lookup_state_instance: LookupState,
      mocked_linter: mock.Mock,
  ) -> None:

    assert lookup_state_instance.cursor == mocked_linter.forest.cursor

  def test_fail__raises_exception(
      self,
      lookup_state_instance: LookupState,
  ) -> None:
    mocked_operation = mock.Mock()
    mocked_operation.lookup_expression.lookups = [mock.Mock()]
    mocked_translated_text = _("mocked_translated_text")

    with pytest.raises(LookupFailure) as exc:
      lookup_state_instance.fail(
          mocked_translated_text,
          mocked_operation,
      )

    assert_is_lookup_failure(
        exc=exc,
        description_t=(mocked_translated_text,),
        lookup=mocked_operation,
    )

  def test_results__getter__retrieves_linter_values(
      self,
      lookup_state_instance: LookupState,
      mocked_linter: mock.Mock,
  ) -> None:

    assert lookup_state_instance.results == mocked_linter.forest.lookup_results

  def test_results__setter__sets_linter_values(
      self,
      lookup_state_instance: LookupState,
      mocked_linter: mock.Mock,
  ) -> None:
    mocked_linter.forest.lookup_results = []

    lookup_state_instance.results = ["1", "2", "3"]

    assert mocked_linter.forest.lookup_results == ["1", "2", "3"]
