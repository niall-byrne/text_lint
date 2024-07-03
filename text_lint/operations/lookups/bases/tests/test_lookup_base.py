"""Test the LookupBase class."""

from unittest import mock

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from ..lookup_base import LookupBase


class TestLookupBase:
  """Test the LookupBase class."""

  def test_initialize__defined__attributes(
      self,
      concrete_lookup_base_instance: LookupBase,
      mocked_lookup_expression: mock.Mock,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "mocked_hint_lookup",
        "is_positional": False,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": mocked_lookup_name,
        "operation": "mocked_operation_lookup",
        "requesting_operation_name": mocked_requesting_operation_name,
        "yaml_example": "mocked_yaml_example_lookup",
    }

    assert_operation_attributes(
        concrete_lookup_base_instance,
        attributes,
    )

  def test_initialize__inheritance(
      self,
      concrete_lookup_base_instance: LookupBase,
  ) -> None:
    assert_operation_inheritance(
        concrete_lookup_base_instance,
        bases=(LookupBase,),
    )
