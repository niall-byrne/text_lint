"""Constants for the parameter validation mixin."""

from typing import Any, Callable, Optional, Tuple, Type, Union

TYPES_ALL = (bool, dict, float, int, list, str, tuple)
TYPES_CONTAINER = (dict, list, tuple)
TYPES_NUMERIC = (float, int)

AliasParameterOfType = Optional[Union[
    Type[Any],
    Tuple[Type[Any], "AliasParameterOfType"],
]]
AliasParameterValidator = Tuple[Callable[[Any], bool], ...]
