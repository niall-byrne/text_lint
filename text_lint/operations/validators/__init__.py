"""Parser result validators for text_lint."""

from typing import Dict, Type

from .bases.validator_base import ValidationBase
from .validate_debug import ValidateDebug
from .validate_equal import ValidateEqual

validator_registry: Dict[str, Type[ValidationBase]] = {
    ValidateDebug.operation: ValidateDebug,
    ValidateEqual.operation: ValidateEqual,
}
