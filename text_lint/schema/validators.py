"""SchemaValidators class."""

from typing import TYPE_CHECKING, Dict, Type

from text_lint.operations.validators import validator_registry
from text_lint.schema.bases.section_base import SchemaSectionBase

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.validators.bases.validator_base import (
      ValidatorBase,
  )


class SchemaValidators(SchemaSectionBase["ValidatorBase"]):
  """The validators section of the schema file."""

  operation_classes: Dict[str, Type["ValidatorBase"]] = validator_registry
  entity_name = "validator"
