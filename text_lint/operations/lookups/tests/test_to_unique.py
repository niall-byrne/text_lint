"""Test the UniqueLookup class."""

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
from text_lint.operations.lookups.encoders.unique import UniqueEncoder
from ..bases.lookup_base import LookupBase
from ..to_unique import YAML_EXAMPLE, UniqueLookup


class TestUniqueLookup:
  """Test the UniqueLookup class."""

  def test_initialize__defined__attributes(
      self,
      mocked_lookup_expression: mock.Mock,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      to_unique_lookup_instance: UniqueLookup,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "encoder_class": UniqueEncoder,
        "hint": "select only unique values from a save id",
        "internal_use_only": False,
        "is_positional": False,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": mocked_lookup_name,
        "operation": LOOKUP_TRANSFORMATION_PREFIX + "unique",
        "requesting_operation_name": mocked_requesting_operation_name,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(to_unique_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      to_unique_lookup_instance: UniqueLookup,
  ) -> None:
    assert_is_translated(to_unique_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      to_unique_lookup_instance: UniqueLookup,
  ) -> None:
    assert_operation_inheritance(
        to_unique_lookup_instance,
        bases=(
            LookupBase,
            LookupEncoderBase,
            UniqueLookup,
        ),
    )

  def test_apply__calls_encode_method(
      self,
      to_unique_lookup_instance: UniqueLookup,
      mocked_encode_method: mock.Mock,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.results = "mock_results"

    to_unique_lookup_instance.apply(mocked_state)

    mocked_encode_method.assert_called_once_with("mock_results")

  def test_apply__updates_forest_lookup_results(
      self,
      to_unique_lookup_instance: UniqueLookup,
      mocked_encode_method: mock.Mock,
      mocked_state: mock.Mock,
  ) -> None:
    to_unique_lookup_instance.apply(mocked_state)

    assert mocked_state.results == mocked_encode_method.return_value
