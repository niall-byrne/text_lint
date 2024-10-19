"""Shared parameter validator factories."""

import re
from functools import lru_cache
from typing import Any, Callable, Dict, List, Pattern, Tuple, Union

AliasContainerType = Union[Dict[Any, Any], List[Any], Tuple[Any, ...]]
AliasConversionFunction = Callable[[Any], Any]

noop_conversion: AliasConversionFunction = lambda value: value


@lru_cache()
def convert_to_selection(index: int) -> Callable[[AliasContainerType], Any]:
  return lambda value: value[index]


@lru_cache()
def create_is_equal(
    target: Any,
    conversion_function: AliasConversionFunction = noop_conversion,
) -> Callable[[Any], bool]:
  return lambda value: conversion_function(value) == target


@lru_cache()
def create_is_greater_than_or_equal(
    threshold: Union[float, int],
    conversion_function: AliasConversionFunction = noop_conversion,
) -> Callable[[Any], bool]:
  return lambda value: conversion_function(value) >= threshold


@lru_cache()
def create_is_in(container: Tuple[Any, ...]) -> Callable[[Any], bool]:
  return lambda value: value in container


@lru_cache()
def create_is_less_than_or_equal(
    threshold: Union[float, int],
    conversion_function: AliasConversionFunction = noop_conversion,
) -> Callable[[Any], bool]:
  return lambda value: conversion_function(value) <= threshold


@lru_cache()
def create_matches_regex(pattern: Pattern[Any]) -> Callable[[Any], bool]:
  return lambda value: bool(re.match(pattern, value))
