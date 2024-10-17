"""Shared parameter validators."""

import re
from functools import lru_cache
from typing import Any, Callable

from text_lint import config


@lru_cache
def create_greater_than_or_equal(
    threshold: int,
    conversion_function: Callable[[Any], int] = int,
) -> Callable[[Any], bool]:
  return lambda value: conversion_function(value) >= threshold


def is_valid_save_id(value: Any) -> bool:
  if re.match(config.SAVED_NAME_REGEX, value):
    return True
  return False
