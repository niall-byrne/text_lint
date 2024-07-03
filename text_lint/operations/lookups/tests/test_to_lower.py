"""Test the LowerLookup class."""
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
from text_lint.operations.lookups.encoders.lower import LowerCaseEncoder
from ..bases.lookup_base import LookupBase
from ..to_lower import YAML_EXAMPLE, LowerLookup


class TestLowerLookup:
  """Test the LowerLookup class."""

  def test_initialize__defined__attributes(
      self,
      to_lower_lookup_instance: LowerLookup,
      mocked_lookup_name: str,
      mocked_requesting_operation_name: str,
      mocked_result_set: mock.Mock,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "encoder_class": LowerCaseEncoder,
        "hint": "convert the saved result's values to lowercase",
        "lookup_name": mocked_lookup_name,
        "operation": LOOKUP_TRANSFORMATION_PREFIX + "lower",
        "requesting_operation_name": mocked_requesting_operation_name,
        "result_set": mocked_result_set,
        "yaml_example": YAML_EXAMPLE,
    }

    assert_operation_attributes(to_lower_lookup_instance, attributes)

  def test_initialize__translations(
      self,
      to_lower_lookup_instance: LowerLookup,
  ) -> None:
    assert_is_translated(to_lower_lookup_instance.hint)

  def test_initialize__inheritance(
      self,
      to_lower_lookup_instance: LowerLookup,
  ) -> None:
    assert_operation_inheritance(
        to_lower_lookup_instance,
        bases=(
            LookupBase,
            LookupEncoderBase,
            LowerLookup,
        ),
    )

  def test_apply__calls_encode_method(
      self,
      to_lower_lookup_instance: LowerLookup,
      mocked_encode_method: mock.Mock,
      mocked_controller: mock.Mock,
      mocked_trees_woods: mock.Mock,
  ) -> None:
    mocked_controller.forest.lookup_results = "mock_results"
    mocked_controller.forest.cursor.location = mocked_trees_woods

    to_lower_lookup_instance.apply(mocked_controller)

    mocked_encode_method.assert_called_once_with("mock_results")

  def test_apply__updates_forest_lookup_results(
      self,
      to_lower_lookup_instance: LowerLookup,
      mocked_encode_method: mock.Mock,
      mocked_controller: mock.Mock,
      mocked_trees_woods: mock.Mock,
  ) -> None:
    mocked_controller.forest.cursor.location = mocked_trees_woods

    to_lower_lookup_instance.apply(mocked_controller)

    assert mocked_controller.forest.lookup_results == (
        mocked_encode_method.return_value
    )
