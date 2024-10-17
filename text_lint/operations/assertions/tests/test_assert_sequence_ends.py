"""Test AssertSequenceEnds class."""

from unittest import mock

from text_lint.__helpers__.assertion import assert_assertion_attributes
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    AliasParameterDefinitions,
    assert_operation_inheritance,
    assert_parameter_schema,
    spy_on_validate_parameters,
)
from text_lint.__helpers__.translations import (
    assert_is_translated,
    assert_is_translated_yaml_example,
)
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from ..assert_sequence_ends import (
    YAML_EXAMPLE,
    YAML_EXAMPLE_COMPONENTS,
    AssertSequenceEnds,
)


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
    assert_is_translated_yaml_example(
        assert_sequence_ends_instance.yaml_example,
        YAML_EXAMPLE_COMPONENTS,
        notes=True,
    )

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

  @spy_on_validate_parameters(AssertSequenceEnds)
  def test_initialize__parameter_validation(
      self,
      validate_parameters_spy: mock.Mock,
      assert_sequence_ends_instance: AssertSequenceEnds,
      base_parameter_definitions: AliasParameterDefinitions,
  ) -> None:
    del base_parameter_definitions["save"]

    assert_parameter_schema(
        instance=assert_sequence_ends_instance,
        parameter_definitions=base_parameter_definitions,
    )
    validate_parameters_spy.assert_called_once_with(
        assert_sequence_ends_instance
    )
