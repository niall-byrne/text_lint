"""Test scenarios for the linter class."""
# pylint: disable=redefined-outer-name

from typing import Any, Type

import pytest

__all__ = (
    "callable_float_schema",
    "complex_dict_schema",
    "complex_list_schema",
    "simple_bool_schema",
    "simple_dict_schema",
    "simple_float_schema",
    "simple_int_schema",
    "simple_list_schema",
    "simple_optional_schema",
    "simple_str_schema",
)


@pytest.fixture
def simple_bool_schema() -> Type[Any]:

  class Parameters:
    name = {"type": str}
    identifier = {"type": bool}

  return Parameters


@pytest.fixture
def simple_dict_schema() -> Type[Any]:

  class Parameters:
    name = {"type": str, "optional": False}
    identifier = {"type": dict, "optional": False}

  return Parameters


@pytest.fixture
def simple_float_schema() -> Type[Any]:

  class Parameters:
    name = {"type": str, "optional": False}
    identifier = {"type": float, "optional": False}

  return Parameters


@pytest.fixture
def simple_int_schema() -> Type[Any]:

  class Parameters:
    name = {"type": str, "optional": False}
    identifier = {"type": int, "optional": False}

  return Parameters


@pytest.fixture
def simple_list_schema() -> Type[Any]:

  class Parameters:
    name = {"type": str, "optional": False}
    identifier = {"type": list, "optional": False}

  return Parameters


@pytest.fixture
def simple_optional_schema() -> Type[Any]:

  class Parameters:
    name = {"type": str, "optional": False}
    identifier = {"type": str, "optional": True}

  return Parameters


@pytest.fixture
def simple_str_schema() -> Type[Any]:

  class Parameters:
    name = {"type": str, "optional": False}
    identifier = {"type": str, "optional": False}

  return Parameters


@pytest.fixture
def callable_float_schema() -> Type[Any]:

  class Parameters:
    name = {"type": str, "optional": False}
    identifier = {
        "type": float,
        "optional": False,
        "validators": [
            lambda value: value > 1,
            lambda value: value < 10,
        ]
    }

  return Parameters


@pytest.fixture
def complex_list_schema() -> Type[Any]:

  class Parameters:
    name = {"type": str, "optional": False}
    identifier = {"type": list, "of": str, "optional": False}

  return Parameters


@pytest.fixture
def complex_dict_schema() -> Type[Any]:

  class Parameters:
    name = {"type": str, "optional": False}
    identifier = {"type": dict, "of": (str, float), "optional": False}

  return Parameters
