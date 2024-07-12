"""Test AssertSequenceEnds class."""

from text_lint.__helpers__.assertion import assert_assertion_attributes
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from ..assert_sequence_ends import YAML_EXAMPLE, AssertSequenceEnds


class TestAssertSequenceEnds:
  """Test the AssertSequenceEnds class."""

  def test_initialize__defined__attributes(
      self,
      assert_sequence_ends_instance: AssertSequenceEnds,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "reserved",
        "internal_use_only": True,
        "name": "example assert sequence ends assertion",
        "operation": "assert_sequence_ends",
        "save": None,
        "splits": {},
        "yaml_example": YAML_EXAMPLE,
    }

    assert_assertion_attributes(assert_sequence_ends_instance, attributes)

  def test_initialize__translations(
      self,
      assert_sequence_ends_instance: AssertSequenceEnds,
  ) -> None:
    assert_is_translated(assert_sequence_ends_instance.hint)

  def test_initialize__inheritance(
      self,
      assert_sequence_ends_instance: AssertSequenceEnds,
  ) -> None:
    assert_operation_inheritance(
        assert_sequence_ends_instance,
        bases=(
            AssertionBase,
            AssertSequenceEnds,
        ),
    )
