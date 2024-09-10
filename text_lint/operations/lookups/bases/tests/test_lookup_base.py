"""Test the LookupBase class."""

from typing import Type
from unittest import mock

import pytest
from text_lint.__helpers__.lookups import assert_is_lookup_failure
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.lookups import LookupFailure
from ..lookup_base import AliasLookupParams, LookupBase


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
        "internal_use_only": False,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": mocked_lookup_name,
        "lookup_params": [],
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

  def test_initialize__translations(
      self,
      concrete_lookup_base_instance: LookupBase,
  ) -> None:
    assert_is_translated(
        concrete_lookup_base_instance.msg_fmt_unexpected_parameters
    )

  @pytest.mark.parametrize("invalid_params", (["1"], ["A", "B"]))
  def test_initialize__unexpected_parameters__raises_exception(
      self,
      concrete_lookup_base_instance: LookupBase,
      concrete_lookup_base_class: Type[LookupBase],
      invalid_params: "AliasLookupParams",
  ) -> None:
    with pytest.raises(LookupFailure) as exc:
      concrete_lookup_base_class(
          concrete_lookup_base_instance.lookup_name,
          concrete_lookup_base_instance.lookup_expression,
          invalid_params,
          concrete_lookup_base_instance.requesting_operation_name,
      )

    assert_is_lookup_failure(
        exc=exc,
        description_t=(
            LookupBase.msg_fmt_unexpected_parameters,
            invalid_params,
        ),
        lookup=concrete_lookup_base_instance
    )
