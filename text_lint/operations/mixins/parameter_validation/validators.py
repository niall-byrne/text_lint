"""Shared parameter validators."""

import re
from functools import lru_cache
from typing import Any, Callable, Pattern, Tuple


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
def create_matches_regex(pattern: Pattern[Any]) -> Callable[[Any], bool]:
  return lambda value: bool(re.match(pattern, value))
