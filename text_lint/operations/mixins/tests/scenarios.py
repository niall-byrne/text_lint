"""Test scenarios for the linter class."""
# pylint: disable=redefined-outer-name

import pytest
from typing import Type, Any

__all__ = (
    "complex_dict_schema",
    "complex_list_schema",
    "simple_bool_schema",
    "simple_dict_schema",
    "simple_float_schema",
    "simple_list_schema",
    "simple_optional_schema",
    "simple_str_schema",
)


@pytest.fixture
def simple_bool_schema() -> Type[Any]:
  class Schema:
    name = {"type": str}
    identifier = {"type": bool}

  return Schema


@pytest.fixture
def simple_dict_schema() -> Type[Any]:
  class Schema:
    name = {"type": str, "optional": False}
    identifier = {"type": dict, "optional": False}

  return Schema


@pytest.fixture
def simple_float_schema() -> Type[Any]:
  class Schema:
    name = {"type": str, "optional": False}
    identifier = {"type": float, "optional": False}

  return Schema


@pytest.fixture
def simple_list_schema() -> Type[Any]:

  class Schema:
    name = {"type": str, "optional": False}
    identifier = {"type": list, "optional": False}

  return Schema


@pytest.fixture
def simple_optional_schema() -> Type[Any]:
  class Schema:
    name = {"type": str, "optional": False}
    identifier = {"type": str, "optional": True}

  return Schema


@pytest.fixture
def simple_str_schema() -> Type[Any]:
  class Schema:
    name = {"type": str, "optional": False}
    identifier = {"type": str, "optional": False}

  return Schema


@pytest.fixture
def complex_list_schema() -> Type[Any]:

  class Schema:
    name = {"type": str, "optional": False}
    identifier = {"type": list, "of": str, "optional": False}

  return Schema


@pytest.fixture
def complex_dict_schema() -> Type[Any]:

  class Schema:
    name = {"type": str, "optional": False}
    identifier = {"type": dict, "of": (str, float), "optional": False}

  return Schema
