"""Validator operations for text_lint."""

from typing import Dict, Type

from .bases.validator_base import ValidatorBase
from .validate_combine import ValidateCombine
from .validate_debug import ValidateDebug
from .validate_equal import ValidateEqual
from .validate_expression import ValidateExpression
from .validate_membership import ValidateMembership
from .validate_not_equal import ValidateNotEqual
from .validate_not_membership import ValidateNotMembership

validator_registry: Dict[str, Type[ValidatorBase]] = {
    ValidateCombine.operation: ValidateCombine,
    ValidateDebug.operation: ValidateDebug,
    ValidateEqual.operation: ValidateEqual,
    ValidateExpression.operation: ValidateExpression,
    ValidateMembership.operation: ValidateMembership,
    ValidateNotEqual.operation: ValidateNotEqual,
    ValidateNotMembership.operation: ValidateNotMembership,
}
