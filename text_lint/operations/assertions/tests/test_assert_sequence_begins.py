"""Test AssertSequenceBegins class."""

from typing import TYPE_CHECKING, List
from unittest import mock

import pytest
from text_lint.__helpers__.assertion import assert_assertion_attributes
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOP_COUNT, NEW_LINE
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from ..assert_sequence_begins import YAML_EXAMPLE, AssertSequenceBegins

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.schema import AliasYamlOperation


class TestAssertSequenceBegins:
  """Test the AssertSequenceBegins class."""

  def test_initialize__defined__attributes(
      self,
      assert_sequence_begins_instance: AssertSequenceBegins,
      mocked_nested_assertions: List[mock.Mock],
  ) -> None:
    attributes: AliasOperationAttributes = {
        "count": 2,
        "hint": "identify a repeating sequence of assertions",
        "internal_use_only": False,
        "name": "example assert sequence begins assertion",
        "operation": "assert_sequence_begins",
        "assertions": mocked_nested_assertions,
        "save": None,
        "splits": {},
        "yaml_example": YAML_EXAMPLE,
    }

    assert_assertion_attributes(assert_sequence_begins_instance, attributes)

  def test_initialize__translations(
      self,
      assert_sequence_begins_instance: AssertSequenceBegins,
  ) -> None:
    assert_is_translated(assert_sequence_begins_instance.hint)
    assert_is_translated(
        assert_sequence_begins_instance.
        msg_fmt_unexpected_assertions_after_eof_sequence
    )

  def test_initialize__inheritance(
      self,
      assert_sequence_begins_instance: AssertSequenceBegins,
  ) -> None:
    assert_operation_inheritance(
        assert_sequence_begins_instance,
        bases=(
            AssertionBase,
            AssertSequenceBegins,
        ),
    )

  @pytest.mark.parametrize("count", [LOOP_COUNT, 2, 4])
  def test_apply__infinite_or_bound_count__calls_loop(
      self,
      assert_sequence_begins_instance: AssertSequenceBegins,
      mocked_state: mock.Mock,
      count: int,
  ) -> None:
    setattr(assert_sequence_begins_instance, "count", count)

    assert_sequence_begins_instance.apply(mocked_state)

    mocked_state.loop.assert_called_with(
        assert_sequence_begins_instance.assertions,
        assert_sequence_begins_instance.count
    )

  @pytest.mark.parametrize("count", [1, 2, 3])
  def test_schema_validator__bound__is_last__does_not_raise_exception(
      self,
      mocked_operation_definitions: List["AliasYamlOperation"],
      mocked_operation_instances: List[AssertionBase],
      mocked_schema: mock.Mock,
      assert_sequence_begins_instance: AssertSequenceBegins,
      count: int,
  ) -> None:
    setattr(assert_sequence_begins_instance, "count", count)

    assert_sequence_begins_instance.schema_validator(
        schema_assertion_index=len(mocked_operation_instances) - 1,
        schema_assertion_instances=mocked_operation_instances,
        schema_assertion_definitions=mocked_operation_definitions,
        schema=mocked_schema,
    )

  @pytest.mark.parametrize("count", [1, 2, 3])
  def test_schema_validator__bound__is_not_last__does_not_raise_exception(
      self,
      mocked_operation_definitions: List["AliasYamlOperation"],
      mocked_operation_instances: List[AssertionBase],
      mocked_schema: mock.Mock,
      assert_sequence_begins_instance: AssertSequenceBegins,
      count: int,
  ) -> None:
    setattr(assert_sequence_begins_instance, "count", count)

    assert_sequence_begins_instance.schema_validator(
        schema_assertion_index=0,
        schema_assertion_instances=mocked_operation_instances,
        schema_assertion_definitions=mocked_operation_definitions,
        schema=mocked_schema,
    )

  def test_schema_validator__infinite__is_last__does_not_raise_exception(
      self,
      mocked_operation_definitions: List["AliasYamlOperation"],
      mocked_operation_instances: List[AssertionBase],
      mocked_schema: mock.Mock,
      assert_sequence_begins_instance: AssertSequenceBegins,
  ) -> None:
    setattr(assert_sequence_begins_instance, "count", LOOP_COUNT)

    assert_sequence_begins_instance.schema_validator(
        schema_assertion_index=len(mocked_operation_instances) - 1,
        schema_assertion_instances=mocked_operation_instances,
        schema_assertion_definitions=mocked_operation_definitions,
        schema=mocked_schema,
    )

  def test_schema_validator__infinite__is_not_last__raises_exception(
      self,
      mocked_operation_definitions: List["AliasYamlOperation"],
      mocked_operation_instances: List[AssertionBase],
      mocked_nested_assertions: List[mock.Mock],
      mocked_schema: mock.Mock,
      assert_sequence_begins_instance: AssertSequenceBegins,
  ) -> None:
    mocked_schema_error = "mocked_schema_error"
    mocked_schema.create_exception.return_value = Exception(mocked_schema_error)
    setattr(assert_sequence_begins_instance, "count", LOOP_COUNT)

    with pytest.raises(Exception) as exc:
      assert_sequence_begins_instance.schema_validator(
          schema_assertion_index=0,
          schema_assertion_instances=mocked_operation_instances,
          schema_assertion_definitions=mocked_operation_definitions,
          schema=mocked_schema,
      )

    mocked_schema.create_exception.assert_called_once_with(
        description=(
            assert_sequence_begins_instance.
            msg_fmt_unexpected_assertions_after_eof_sequence
        ).format(0) + NEW_LINE,
        operation_definition=mocked_operation_definitions[0]
    )
    assert mocked_operation_definitions[0] == {
        "definition":
            1,
        "assertions":
            [assertion.operation for assertion in mocked_nested_assertions],
    }
    assert str(exc.value) == mocked_schema_error
