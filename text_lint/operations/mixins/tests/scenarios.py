"""Test scenarios for the linter class."""
# pylint: disable=redefined-outer-name

import pytest
from ..parameter_validation import AliasParameterSchema

__all__ = (
    "complex_dict_schema",
    "complex_list_schema",
    "simple_bool_schema",
    "simple_dict_schema",
    "simple_float_schema",
    "simple_list_schema",
    "simple_none_schema",
    "simple_str_schema",
)


@pytest.fixture
def simple_bool_schema() -> AliasParameterSchema:
  return {"name": str, "identifier": bool}


@pytest.fixture
def simple_dict_schema() -> AliasParameterSchema:
  return {"name": str, "identifier": dict}


@pytest.fixture
def simple_float_schema() -> AliasParameterSchema:
  return {"name": str, "identifier": float}


@pytest.fixture
def simple_list_schema() -> AliasParameterSchema:
  return {"name": str, "identifier": list}


@pytest.fixture
def simple_none_schema() -> AliasParameterSchema:
  return {"name": str, "identifier": None}


@pytest.fixture
def simple_str_schema() -> AliasParameterSchema:
  return {"name": str, "identifier": str}


@pytest.fixture
def complex_list_schema() -> AliasParameterSchema:
  return {
      "name": str,
      "identifier": (list, str),
  }


@pytest.fixture
def complex_dict_schema() -> AliasParameterSchema:
  return {
      "name": str,
      "identifier": (dict, (str, float)),
  }
