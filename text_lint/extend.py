"""External extension support.

User defined Operations or Mathematical Expressions should import from
this module to ensure forward compatibility.

.. list-table::
   :class: tight-table full-width-table
   :widths: 30 50
   :header-rows: 1

   * - Class
     - Subclass Use Case
   * - AssertionBase
     - Derive from this class to create assertion operations.
   * - AssertionRegexBase
     - Derive from this class to create assertion operations with regexes.
   * - ExpressionBase
     - Derive from this class to create mathematics operations.
   * - LookupBase
     - Derive from this class to create lookup operations.
   * - LookupEncoderBase
     - Derive from this class to create lookup operations that encode values.
   * - ValidatorBase
     - Derive from this class to create validator operations.
   * - ValidationComparisonBase
     - Derive from this class to create validator operations with comparisons.

.. list-table::
   :class: tight-table full-width-table
   :widths: 30 50
   :header-rows: 1

   * - Class
     - Typehint Use Case
   * - AssertionState
     - Use to typehint state in AssertionBase derived classes.
   * - LookupState
     - Use to typehint state in LookupState derived classes.
   * - ValidatorState
     - Use to typehint state in ValidatorState derived classes.
"""
# pylint: disable=unused-import

from text_lint.linter.states import AssertionState, LookupState, ValidatorState
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.assertions.bases.assertion_regex_base import (
    AssertionRegexBase,
)
from text_lint.operations.bases.operation_base import OperationBase
from text_lint.operations.lookups.bases.lookup_base import LookupBase
from text_lint.operations.lookups.bases.lookup_encoder_base import (
    LookupEncoderBase,
)
from text_lint.operations.validators.bases.validator_base import ValidatorBase
from text_lint.operations.validators.bases.validator_comparison_base import (
    ValidationComparisonBase,
)
from text_lint.operations.validators.expressions.bases.expression_base import (
    ExpressionBase,
)
