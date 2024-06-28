"""Validator operations for text_lint."""

from typing import Dict, Type

from .bases.validator_base import ValidatorBase
from .validate_debug import ValidateDebug

validator_registry: Dict[str, Type[ValidatorBase]] = {
    ValidateDebug.operation: ValidateDebug
}
