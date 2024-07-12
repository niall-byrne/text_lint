"""Test the JsonLookup class."""

from unittest import mock

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.operations.lookups.bases.lookup_encoder_base import (
    LookupEncoderBase,
)
from text_lint.operations.lookups.encoders.tree import ResultTreeEncoder
from ..as_json import YAML_EXAMPLE, JsonLookup
from ..bases.lookup_base import LookupBase


class TestJsonLookup:
  """Test the JsonLookup class."""

  def test_initialize__defined__attributes(
      self,
      mocked_lookup_name: str,
      mocked_lookup_expression: mock.Mock,
      mocked_requesting_operation_name: str,
      as_json_lookup_instance: JsonLookup,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "encoder_class": ResultTreeEncoder,
        "hint": "create a JSON representation of a save id",
        "internal_use_only": False,
        "is_positional": True,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": mocked_lookup_name,
        "operation": "as_json",
        "requesting_operation_name": mocked_requesting_operation_name,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(as_json_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      as_json_lookup_instance: JsonLookup,
  ) -> None:
    assert_is_translated(as_json_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      as_json_lookup_instance: JsonLookup,
  ) -> None:
    assert_operation_inheritance(
        as_json_lookup_instance,
        bases=(
            LookupBase,
            LookupEncoderBase,
            JsonLookup,
        ),
    )

  def test_apply__calls_encode_method(
      self,
      as_json_lookup_instance: JsonLookup,
      mocked_encode_method: mock.Mock,
      mocked_state: mock.Mock,
      mocked_trees_woods: mock.Mock,
  ) -> None:
    mocked_state.cursor.location = mocked_trees_woods

    as_json_lookup_instance.apply(mocked_state)

    mocked_encode_method.assert_called_once_with(mocked_state.cursor.location)

  def test_apply__updates_forest_lookup_results(
      self,
      as_json_lookup_instance: JsonLookup,
      mocked_encode_method: mock.Mock,
      mocked_state: mock.Mock,
      mocked_trees_woods: mock.Mock,
  ) -> None:
    mocked_state.cursor.location = mocked_trees_woods

    as_json_lookup_instance.apply(mocked_state)

    assert mocked_state.results == (mocked_encode_method.return_value)
