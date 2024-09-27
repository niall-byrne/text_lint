"""Mathematical expression registry"""

from typing import Dict, Type

from .add import Add
from .bases.expression_base import ExpressionBase
from .divide import Divide
from .exponent import Exponent
from .greater_than import GreaterThan
from .greater_than_or_equal import GreaterThanOrEqual
from .less_than import LessThan
from .less_than_or_equal import LessThanOrEqual
from .multiply import Multiply
from .subtract import Subtract

expressions_registry: Dict[str, Type[ExpressionBase]] = {
    Add.operator: Add,
    Divide.operator: Divide,
    Exponent.operator: Exponent,
    GreaterThan.operator: GreaterThan,
    GreaterThanOrEqual.operator: GreaterThanOrEqual,
    LessThan.operator: LessThan,
    LessThanOrEqual.operator: LessThanOrEqual,
    Multiply.operator: Multiply,
    Subtract.operator: Subtract,
}
