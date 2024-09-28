"""Test the SchemaAssertions class."""

from typing import TYPE_CHECKING, List
from unittest import mock

import pytest
from text_lint.__fixtures__.mocks import AliasMethodMocker
from text_lint.__helpers__.translations import (
    as_translation,
    assert_is_translated,
)
from text_lint.operations.assertions import (
    AssertSequenceBegins,
    AssertSequenceEnds,
    assertion_registry,
)
from text_lint.utilities.translations import f
from ..assertions import SchemaAssertions
from .fixtures import schemas

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )
  from text_lint.schema import AliasYamlOperation


class TestSchemaAssertions:
  """Test the SchemaAssertions class."""

  def test_attributes(self) -> None:
    assert SchemaAssertions.automated_section_end_assertion_name == \
        as_translation("Automated End of Sequence")
    assert SchemaAssertions.operation_classes == assertion_registry
    assert SchemaAssertions.entity_name == "assertion"

  def test_translated_attributes(self,) -> None:
    assert_is_translated(SchemaAssertions.automated_section_end_assertion_name)
    assert_is_translated(SchemaAssertions.msg_fmt_no_nested_assertions)

  def test_hook_load_operation_instances__calls_schema_validator(
      self,
      mocked_operation_definitions: List["AliasYamlOperation"],
      mocked_operation_instances: List["AssertionBase"],
      mocked_schema: mock.Mock,
  ) -> None:
    instance = SchemaAssertions(mocked_schema)

    instance.hook_load_operation_instances(
        mocked_operation_instances,
        mocked_operation_definitions,
    )

    for index, assertion in enumerate(mocked_operation_instances):
      if isinstance(assertion, mock.Mock):
        assert index < len(mocked_operation_instances) - 1
        assertion.schema_validator.assert_called_once_with(
            index,
            mocked_operation_instances,
            mocked_operation_definitions,
            mocked_schema,
        )
      else:
        assert index == len(mocked_operation_instances) - 1
        assert isinstance(assertion, AssertSequenceEnds)

  def test_hook_load_operation_instances__appends_assert_sequence_end(
      self,
      mocked_operation_definitions: List["AliasYamlOperation"],
      mocked_operation_instances: List["AssertionBase"],
      mocked_schema: mock.Mock,
  ) -> None:
    instance = SchemaAssertions(mocked_schema)

    result = instance.hook_load_operation_instances(
        mocked_operation_instances,
        mocked_operation_definitions,
    )

    assert len(result) == 3
    assert result[0] == mocked_operation_instances[0]
    assert result[1] == mocked_operation_instances[1]
    assert isinstance(result[2], AssertSequenceEnds)
    assert result[2].name == \
           SchemaAssertions.automated_section_end_assertion_name

  def test_hook_create_operation_instance__nested__appends_nested_assertions(
      self,
      mocked_schema: mock.Mock,
      method_mocker: AliasMethodMocker,
  ) -> None:
    mocked_operation_class = mock.Mock()
    mocked_operation_class.operation = AssertSequenceBegins.operation
    instance = SchemaAssertions(mocked_schema)
    mocked_load_method = method_mocker(instance.load)

    result = instance.hook_create_operation_instance(
        mocked_operation_class,
        {"assertions": ["mocked_yaml_content"]},
    )

    assert result == {"assertions": mocked_load_method.return_value}
    mocked_load_method.assert_called_once_with(["mocked_yaml_content"])

  def test_hook_create_operation_instance__empty_nested__raises_exception(
      self,
      mocked_schema: mock.Mock,
  ) -> None:
    mocked_schema.create_exception.side_effect = Exception
    mocked_operation_class = mock.Mock()
    mocked_operation_class.operation = AssertSequenceBegins.operation
    instance = SchemaAssertions(mocked_schema)

    with pytest.raises(Exception):
      instance.hook_create_operation_instance(
          mocked_operation_class,
          {"assertions": []},
      )

    mocked_schema.create_exception.assert_called_once_with(
        description=f(instance.msg_fmt_no_nested_assertions, nl=1),
        operation_definition={"assertions": []}
    )

  def test_hook_create_operation_instance__non_nested__does_not_append(
      self,
      mocked_schema: mock.Mock,
      method_mocker: AliasMethodMocker,
  ) -> None:
    mocked_operation_class = mock.Mock()
    mocked_operation_class.operation = AssertSequenceEnds.operation
    instance = SchemaAssertions(mocked_schema)
    mocked_load_method = method_mocker(instance.load)

    result = instance.hook_create_operation_instance(
        mocked_operation_class,
        schemas.one_simple_assertion["assertions"][0],
    )

    assert result == schemas.one_simple_assertion["assertions"][0]
    mocked_load_method.assert_not_called()
