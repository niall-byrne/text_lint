"""Validator operations for text_lint."""

from typing import Dict, Type

from .bases.validator_base import ValidatorBase
from .validate_combine import ValidateCombine
from .validate_debug import ValidateDebug
from .validate_equal import ValidateEqual

validator_registry: Dict[str, Type[ValidatorBase]] = {
    ValidateCombine.operation: ValidateCombine,
    ValidateDebug.operation: ValidateDebug,
    ValidateEqual.operation: ValidateEqual,
}
