"""Test the JsonLookup class."""

from unittest import mock

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.operations.lookups.bases.lookup_encoder_base import (
    LookupEncoderBase,
)
from text_lint.operations.lookups.encoders.tree import ResultTreeEncoder
from ..bases.lookup_base import LookupBase
from ..to_json import JsonLookup


class TestJsonLookup:
  """Test the JsonLookup class."""

  def test_initialize__defined__attributes(
      self,
      to_json_lookup_instance: JsonLookup,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "encoder_class": ResultTreeEncoder,
        "hint": "create a JSON representation of the saved result",
        "lookup_name": mocked_lookup_name,
        "operation": LOOKUP_TRANSFORMATION_PREFIX + "json",
        "requesting_operation_name": mocked_requesting_operation_name,
        "result_set": mocked_result_set,
    }

    assert_operation_attributes(to_json_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      to_json_lookup_instance: JsonLookup,
  ) -> None:
    assert_is_translated(to_json_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      to_json_lookup_instance: JsonLookup,
  ) -> None:
    assert_operation_inheritance(
        to_json_lookup_instance,
        bases=(
            LookupBase,
            LookupEncoderBase,
            JsonLookup,
        ),
    )

  def test_apply__calls_encode_method(
      self,
      to_json_lookup_instance: JsonLookup,
      mocked_encode_method: mock.Mock,
      mocked_controller: mock.Mock,
      mocked_trees_woods: mock.Mock,
  ) -> None:
    mocked_controller.forest.cursor.location = mocked_trees_woods

    to_json_lookup_instance.apply(mocked_controller)

    mocked_encode_method.assert_called_once_with(
        mocked_controller.forest.cursor.location
    )

  def test_apply__updates_forest_lookup_results(
      self,
      to_json_lookup_instance: JsonLookup,
      mocked_encode_method: mock.Mock,
      mocked_controller: mock.Mock,
      mocked_trees_woods: mock.Mock,
  ) -> None:
    mocked_controller.forest.cursor.location = mocked_trees_woods

    to_json_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.lookup_results == (
        mocked_encode_method.return_value
    )
