"""Test the LookupExpression class."""
from typing import List
from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    assert_parameter_schema,
    spy_on_validate_parameters,
)
from ..lookup_expression import LookupExpression


class TestLookupExpression:
  """Test the LookupExpression class."""

  @pytest.mark.usefixtures("mocked_parse_lookup_expression")
  def test_initialize__attributes(
      self,
      mocked_source: str,
      mocked_parsed_lookups: List[mock.Mock],
  ) -> None:
    mocked_lookup = "source_name.lookup_operation_a().lookup_operation_b()"

    instance = LookupExpression(mocked_lookup)

    assert instance.name == mocked_lookup
    assert instance.source == mocked_source
    assert instance.lookups == mocked_parsed_lookups

  @spy_on_validate_parameters(LookupExpression)
  def test_initialize__parameters(
      self,
      validate_parameters_spy: mock.Mock,
  ) -> None:
    mocked_lookup = "source_name.lookup_operation_a().lookup_operation_b()"

    instance = LookupExpression(mocked_lookup)

    assert_parameter_schema(
        instance=instance,
        parameter_definitions={
            "name": {
                "type": str
            },
        },
    )
    validate_parameters_spy.assert_called_once_with(instance)

  def test_initialize__calls_parse_lookup_expression(
      self,
      mocked_parse_lookup_expression: mock.Mock,
  ) -> None:
    mocked_lookup = "source_name.lookup_operation_a().lookup_operation_b()"

    _ = LookupExpression(mocked_lookup)

    mocked_parse_lookup_expression.assert_called_once_with(mocked_lookup)
