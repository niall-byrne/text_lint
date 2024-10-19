"""Shared parameter validators."""

import re
from functools import lru_cache
from typing import Any, Callable, Dict, List, Pattern, Tuple, Union

AliasContainerType = Union[Dict[Any, Any], List[Any], Tuple[Any, ...]]


@lru_cache()
def convert_to_selection(index: int) -> Callable[[AliasContainerType], Any]:
  return lambda value: value[index]


@lru_cache()
def create_is_equal(
    target: int,
    conversion_function: Callable[[Any], int] = int,
) -> Callable[[Any], bool]:
  return lambda value: conversion_function(value) == target


@lru_cache()
def create_is_greater_than_or_equal(
    threshold: int,
    conversion_function: Callable[[Any], int] = int,
) -> Callable[[Any], bool]:
  return lambda value: conversion_function(value) >= threshold


@lru_cache()
def create_is_in(container: Tuple[Any, ...]) -> Callable[[Any], bool]:
  return lambda value: value in container


@lru_cache()
def create_is_less_than_or_equal(
    threshold: int,
    conversion_function: Callable[[Any], int] = int,
) -> Callable[[Any], bool]:
  return lambda value: conversion_function(value) <= threshold


@lru_cache()
def create_matches_regex(pattern: Pattern[Any]) -> Callable[[Any], bool]:
  return lambda value: bool(re.match(pattern, value))
