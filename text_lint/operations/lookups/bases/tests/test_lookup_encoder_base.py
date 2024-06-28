"""Test the LookupEncoderBase class."""

from unittest import mock

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
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "encoder_class": mocked_encoder_class,
        "hint": "mocked_hint_lookup_encoder",
        "lookup_name": mocked_lookup_name,
        "operation": "mocked_operation_lookup_encoder",
        "requesting_operation_name": mocked_requesting_operation_name,
        "result_set": mocked_result_set,
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

  def test_encode__calls_json_methods_with_correct_encoder(
      self,
      concrete_lookup_encoder_base_instance: LookupEncoderBase,
      mocked_json_module: mock.Mock,
  ) -> None:
    mocked_object = {"mock": "object"}

    concrete_lookup_encoder_base_instance.encode(mocked_object)

    mocked_json_module.dumps.assert_called_once_with(
        mocked_object,
        cls=concrete_lookup_encoder_base_instance.encoder_class,
    )
    mocked_json_module.loads.assert_called_once_with(
        mocked_json_module.dumps.return_value
    )

  def test_encode__returns_expected_value(
      self,
      concrete_lookup_encoder_base_instance: LookupEncoderBase,
      mocked_json_module: mock.Mock,
  ) -> None:
    mocked_object = {"mock": "object"}

    return_value = concrete_lookup_encoder_base_instance.encode(mocked_object)

    assert return_value == mocked_json_module.loads.return_value
