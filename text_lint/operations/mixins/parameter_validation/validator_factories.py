"""Shared parameter validator factories."""

import re
from functools import lru_cache
from typing import Any, Callable, Dict, List, Pattern, Tuple, Union

AliasContainerType = Union[Dict[Any, Any], List[Any], Tuple[Any, ...]]
AliasConversionFunction = Callable[[Any], Any]

noop_conversion: AliasConversionFunction = lambda value: value


@lru_cache()
def convert_to_selection(index: int) -> Callable[[AliasContainerType], Any]:
  """Create a validator to access a single value from an index-able attribute.

  :param index: The index to access on the attribute's value.
  :returns: A function to access an attribute's indexed value.
  """
  return lambda value: value[index]


@lru_cache()
def create_is_equal(
    target: Any,
    conversion_function: AliasConversionFunction = noop_conversion,
) -> Callable[[Any], bool]:
  """Create a validator to perform an equality test on an attribute.

  :param target: The value the attribute value will be compared to.
  :param conversion_function: Transform the attribute value before comparison.
  :returns: A function to check an attribute's value for equality.
  """
  return lambda value: conversion_function(value) == target


@lru_cache()
def create_is_greater_than_or_equal(
    threshold: Union[float, int],
    conversion_function: AliasConversionFunction = noop_conversion,
) -> Callable[[Any], bool]:
  """Create a validator to perform a >= test on an attribute.

  :param threshold: The value the attribute value will be compared to.
  :param conversion_function: Transform the attribute value before comparison.
  :returns: A function to check if an attribute's value is >= the target.
  """
  return lambda value: conversion_function(value) >= threshold


@lru_cache()
def create_is_in(container: Tuple[Any, ...]) -> Callable[[Any], bool]:
  """Create a validator to check if an attribute is in set of values.

  :param container: A tuple of values the attribute can be equal to.
  :returns: A function to check if an attribute's value is in a set of values.
  """
  return lambda value: value in container


@lru_cache()
def create_is_less_than_or_equal(
    threshold: Union[float, int],
    conversion_function: AliasConversionFunction = noop_conversion,
) -> Callable[[Any], bool]:
  """Create a validator to perform a <= test on an attribute.

  :param threshold: The value the attribute value will be compared to.
  :param conversion_function: Transform the attribute value before comparison.
  :returns: A function to check if an attribute's value is <= the target.
  """
  return lambda value: conversion_function(value) <= threshold


@lru_cache()
def create_matches_regex(pattern: Pattern[Any]) -> Callable[[Any], bool]:
  """Create a validator to perform a regex match on an attribute.

  :param pattern: The regex pattern to attempt to match the attribute with.
  :returns: A function to check an attribute's value against a regex pattern.
  """
  return lambda value: bool(re.match(pattern, value))
