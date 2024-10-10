"""Test the ParameterValidationMixin class."""

from typing import Any, Type

import pytest
from text_lint.__helpers__.operations import (
    assert_is_invalid_parameter_validation,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.operations import InvalidParameterValidation
from ..parameter_validation import ParameterValidationMixin
from .conftest import PersonClass


class TestParameterValidationMixin:
  """Test the ParameterValidationMixin class."""

  def test_initialize__translations(self) -> None:
    assert_is_translated(
        ParameterValidationMixin.msg_fmt_parameter_invalid_value
    )
    assert_is_translated(
        ParameterValidationMixin.msg_fmt_parameter_invalid_container_description
    )
    assert_is_translated(
        ParameterValidationMixin.msg_fmt_parameter_invalid_container_detail
    )
    assert_is_translated(
        ParameterValidationMixin.
        msg_fmt_parameter_invalid_dictionary_definition_description
    )
    assert_is_translated(
        ParameterValidationMixin.
        msg_fmt_parameter_invalid_dictionary_definition_detail
    )

  @pytest.mark.parametrize(
      "fixture_name,identifier",
      [
          ["simple_bool_schema", True],
          [
              "simple_dict_schema",
              {
                  "key": "value"
              },
          ],
          ["simple_float_schema", 2.0],
          ["simple_list_schema", ["value"]],
          ["simple_optional_schema", None],
          ["simple_str_schema", "id"],
          [
              "complex_dict_schema",
              {
                  "key": 2.0
              },
          ],
          ["complex_list_schema", ["A", "B"]],
      ],
  )
  def test_initialize__vary_schema__passes(
      self,
      concrete_parameter_class: Type[PersonClass],
      fixture_name: str,
      identifier: Any,
      request: pytest.FixtureRequest,
  ) -> None:
    parameter_schema = request.getfixturevalue(fixture_name)
    setattr(concrete_parameter_class, "Schema", parameter_schema)

    concrete_parameter_class(name="string", identifier=identifier)

  @pytest.mark.parametrize(
      "fixture_name,identifier,invalid_value",
      [
          ["simple_bool_schema", "True", "True"],
          ["simple_dict_schema", "{}", "{}"],
          ["simple_float_schema", "2.0", "2.0"],
          ["simple_list_schema", "[]", "[]"],
          ["simple_optional_schema", 1.0, 1.0],
          ["simple_str_schema", None, None],
          [
              "complex_dict_schema",
              {
                  "key": "2.0"
              },
              "2.0",
          ],
          ["complex_list_schema", ["A", None], None],
      ],
  )
  def test_initialize__vary_schema__fails(
      self,
      concrete_parameter_class: Type[PersonClass],
      fixture_name: str,
      identifier: Any,
      invalid_value: Any,
      request: pytest.FixtureRequest,
  ) -> None:
    parameter_schema = request.getfixturevalue(fixture_name)
    setattr(concrete_parameter_class, "Schema", parameter_schema)

    with pytest.raises(TypeError) as exc:
      concrete_parameter_class(name="string", identifier=identifier)

    assert str(exc.value) == (
        ParameterValidationMixin.msg_fmt_parameter_invalid_value.format(
            invalid_value,
            "identifier",
        )
    )

  def test_initialize__invalid_complex_iterable__raises_exception(
      self,
      concrete_parameter_class: Type[PersonClass],
  ) -> None:
    setattr(concrete_parameter_class, "parameters", {"identifier": (str, str)})

    with pytest.raises(InvalidParameterValidation) as exc:
      concrete_parameter_class(name="string", identifier="string")

    assert_is_invalid_parameter_validation(
        exc=exc,
        description_t=(
            ParameterValidationMixin.
            msg_fmt_parameter_invalid_container_description,
        ),
        detail_t=(
            ParameterValidationMixin.msg_fmt_parameter_invalid_container_detail,
            "identifier", str(str)
        ),
        operation_class=concrete_parameter_class,
    )

  def test_initialize__invalid_complex_dict__raises_exception(
      self,
      concrete_parameter_class: Type[PersonClass],
  ) -> None:
    setattr(concrete_parameter_class, "parameters", {"identifier": (dict, str)})

    with pytest.raises(InvalidParameterValidation) as exc:
      concrete_parameter_class(name="string", identifier="string")

    assert_is_invalid_parameter_validation(
        exc=exc,
        description_t=(
            ParameterValidationMixin.
            msg_fmt_parameter_invalid_dictionary_definition_description,
        ),
        detail_t=(
            ParameterValidationMixin.
            msg_fmt_parameter_invalid_dictionary_definition_detail,
            "identifier",
            str(str),
        ),
        operation_class=concrete_parameter_class,
    )
