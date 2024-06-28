"""Test the SchemaValidators class."""

from text_lint.operations.validators import validator_registry
from ..validators import SchemaValidators


class TestSchemaValidators:
  """Test the SchemaValidators class."""

  def test_attributes(self) -> None:
    assert SchemaValidators.operation_classes == validator_registry
    assert SchemaValidators.entity_name == "validator"
