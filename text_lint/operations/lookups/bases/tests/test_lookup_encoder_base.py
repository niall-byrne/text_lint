"""Test the LookupEncoderBase class."""

from typing import Any, Dict
from unittest import mock

import pytest
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from ..lookup_base import LookupBase
from ..lookup_encoder_base import LookupEncoderBase


class TestLookupEncoderBase:
  """Test the LookupEncoderBase class."""

  def test_initialize__defined__attributes(
      self,
      concrete_lookup_encoder_base_instance: LookupEncoderBase,
      mocked_encoder_class: mock.Mock,
      mocked_lookup_expression: mock.Mock,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "encoder_class": mocked_encoder_class,
        "encoder_params": {},
        "hint": "mocked_hint_lookup_encoder",
        "is_positional": False,
        "internal_use_only": False,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": mocked_lookup_name,
        "operation": "mocked_operation_lookup_encoder",
        "requesting_operation_name": mocked_requesting_operation_name,
        "yaml_example": "mocked_yaml_example_lookup_encoder",
    }

    assert_operation_attributes(
        concrete_lookup_encoder_base_instance,
        attributes,
    )

  def test_initialize__inheritance(
      self,
      concrete_lookup_encoder_base_instance: LookupEncoderBase,
  ) -> None:
    assert_operation_inheritance(
        concrete_lookup_encoder_base_instance,
        bases=(LookupBase, LookupEncoderBase),
    )

  @pytest.mark.parametrize(
      "encoder_params", [
          {},
          {
              "param1": "value1"
          },
          {
              "param1": "value1",
              "param2": "value2",
          },
      ]
  )
  def test_encode__vary_params__calls_encoder_class_correctly(
      self,
      concrete_lookup_encoder_base_instance: LookupEncoderBase,
      mocked_encoder_class: mock.Mock,
      encoder_params: Dict[str, Any],
  ) -> None:
    mocked_object = {"mock": "object"}
    concrete_lookup_encoder_base_instance.encoder_params = encoder_params

    concrete_lookup_encoder_base_instance.encode(mocked_object)

    mocked_encoder_class.assert_called_once_with(
        **concrete_lookup_encoder_base_instance.encoder_params
    )
    mocked_encoder_class.return_value.encode.assert_called_once_with(
        mocked_object
    )

  def test_encode__calls_json_loads_correctly(
      self,
      concrete_lookup_encoder_base_instance: LookupEncoderBase,
      mocked_encoder_class: mock.Mock,
      mocked_json_module: mock.Mock,
  ) -> None:
    mocked_object = {"mock": "object"}

    concrete_lookup_encoder_base_instance.encode(mocked_object)

    mocked_json_module.loads.assert_called_once_with(
        mocked_encoder_class.return_value.encode.return_value
    )

  def test_encode__returns_expected_value(
      self,
      concrete_lookup_encoder_base_instance: LookupEncoderBase,
      mocked_json_module: mock.Mock,
  ) -> None:
    mocked_object = {"mock": "object"}

    return_value = concrete_lookup_encoder_base_instance.encode(mocked_object)

    assert return_value == mocked_json_module.loads.return_value
