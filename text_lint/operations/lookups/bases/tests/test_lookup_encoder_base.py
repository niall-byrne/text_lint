"""Test the LookupEncoderBase class."""

from typing import Any, Dict, Type
from unittest import mock

import pytest
from text_lint.__helpers__.lookups import assert_is_lookup_failure
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
    assert_parameter_schema,
    spy_on_validate_parameters,
)
from text_lint.exceptions.lookups import LookupFailure
from text_lint.operations.mixins.parameter_validation import (
    ParameterValidationMixin,
    validators,
)
from ..lookup_base import AliasLookupParams, LookupBase
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
        "lookup_params": [],
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
    assert isinstance(
        concrete_lookup_encoder_base_instance,
        ParameterValidationMixin,
    )
    assert_operation_inheritance(
        concrete_lookup_encoder_base_instance,
        bases=(LookupBase, LookupEncoderBase),
    )

  @spy_on_validate_parameters(LookupEncoderBase)
  def test_initialize__parameter_validation(
      self,
      validate_parameters_spy: mock.Mock,
      concrete_lookup_encoder_base_instance: LookupEncoderBase,
  ) -> None:
    assert_parameter_schema(
        # pylint: disable=duplicate-code
        instance=concrete_lookup_encoder_base_instance,
        parameter_definitions={
            "lookup_name": {
                "type": str
            },
            "lookup_params":
                {
                    "type":
                        list,
                    "validators":
                        [
                            validators.create_is_equal(
                                0,
                                conversion_function=len,
                            ),
                        ],
                }
        }
    )
    validate_parameters_spy.assert_called_once_with(
        concrete_lookup_encoder_base_instance
    )

  @pytest.mark.parametrize("invalid_params", (["1"], ["A", "B"]))
  def test_initialize__unexpected_parameters__raises_exception(
      self,
      concrete_lookup_encoder_base_instance: LookupEncoderBase,
      concrete_lookup_encoder_base_class: Type[LookupEncoderBase],
      invalid_params: "AliasLookupParams",
  ) -> None:
    with pytest.raises(LookupFailure) as exc:
      concrete_lookup_encoder_base_class(
          concrete_lookup_encoder_base_instance.lookup_name,
          concrete_lookup_encoder_base_instance.lookup_expression,
          invalid_params,
          concrete_lookup_encoder_base_instance.requesting_operation_name,
      )

    assert_is_lookup_failure(
        exc=exc,
        description_t=(
            LookupEncoderBase.msg_fmt_invalid_parameters,
            invalid_params,
        ),
        lookup=concrete_lookup_encoder_base_instance
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
