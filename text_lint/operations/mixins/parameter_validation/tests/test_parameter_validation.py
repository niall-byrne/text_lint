"""Test the ParameterValidationMixin class."""

import copy
from typing import Any, Dict, Type

import pytest
from text_lint.__helpers__.operations import (
    assert_is_invalid_parameter_validation,
)
from text_lint.__helpers__.translations import (
    assert_all_translated,
    assert_is_translated,
)
from text_lint.exceptions.operations import InvalidParameterValidation
from text_lint.operations.mixins.parameter_validation import (
    ParameterValidationMixin,
)
from text_lint.operations.mixins.parameter_validation.constants import (
    TYPES_ALL,
    TYPES_CONTAINER,
)
from text_lint.utilities.whitespace import new_line
from .conftest import PersonClass


class TestParameterValidationMixin:
  """Test the ParameterValidationMixin class."""

  def test_initialize__attributes(self) -> None:
    assert ParameterValidationMixin.parameter_definition_keys == (
        "type",
        "of",
        "optional",
        "validators",
    )
    assert ParameterValidationMixin.parameter_schema_class_name == "Parameters"
    assert ParameterValidationMixin.parameter_definition_width == 10

  def test_initialize__translations(self) -> None:
    assert_is_translated(
        ParameterValidationMixin.msg_fmt_parameter_invalid_value
    )
    assert_is_translated(
        ParameterValidationMixin.
        msg_fmt_parameter_invalid_definition_description
    )
    assert_all_translated(
        ParameterValidationMixin.
        msg_fmt_parameter_invalid_definition_detail_tuple
    )

  def test_initialize__no_schema__passes(
      self,
      concrete_parameter_class: Type[PersonClass],
  ) -> None:

    concrete_parameter_class(name="string", identifier="string")

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
          ["simple_float_schema", 1],
          ["simple_float_schema", 2.0],
          ["simple_int_schema", 1],
          ["simple_list_schema", ["value"]],
          ["simple_optional_schema", None],
          ["callable_float_schema", 2.0],
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
    setattr(
        concrete_parameter_class,
        ParameterValidationMixin.parameter_schema_class_name,
        parameter_schema,
    )

    concrete_parameter_class(name="string", identifier=identifier)

  @pytest.mark.parametrize(
      "fixture_name,identifier,invalid_value",
      [
          ["simple_bool_schema", "True", "True"],
          ["simple_dict_schema", "{}", "{}"],
          ["simple_float_schema", "2.x", "2.x"],
          ["simple_int_schema", 2.2, 2.2],
          ["simple_list_schema", "[]", "[]"],
          ["simple_optional_schema", 1.0, 1.0],
          ["simple_str_schema", None, None],
          ["callable_float_schema", 0.5, 0.5],
          [
              "complex_dict_schema",
              {
                  "key": "2.x"
              },
              "2.x",
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
    setattr(
        concrete_parameter_class,
        ParameterValidationMixin.parameter_schema_class_name,
        parameter_schema,
    )

    with pytest.raises(TypeError) as exc:
      concrete_parameter_class(name="string", identifier=identifier)

    assert str(exc.value) == (
        ParameterValidationMixin.msg_fmt_parameter_invalid_value.format(
            invalid_value,
            "identifier",
        )
    )

  @pytest.mark.parametrize(
      "fixture_name,invalid_schema",
      [
          [
              "complex_list_schema",
              {
                  "type2": float
              },
          ],
          [
              "complex_list_schema",
              {
                  "type": str,
                  "optional": None
              },
          ],
          [
              "complex_list_schema",
              {
                  "type": None
              },
          ],
          [
              "complex_list_schema",
              {
                  "type": (str, int)
              },
          ],
          [
              "complex_list_schema",
              {
                  "type": str,
                  "of": str
              },
          ],
          [
              "complex_list_schema",
              {
                  "type": list,
                  "of": (str,)
              },
          ],
          [
              "complex_list_schema",
              {
                  "type": dict,
                  "of": (str,)
              },
          ],
          [
              "complex_list_schema",
              {
                  "type": dict,
                  "of": str
              },
          ],
          [
              "complex_list_schema",
              {
                  "type": "int"
              },
          ],
          [
              "complex_list_schema",
              {
                  "type": list,
                  "validator": list,
              },
          ],
          [
              "complex_list_schema",
              {
                  "type": list,
                  "validator": (list,),
              },
          ],
      ],
  )
  def test_initialize__vary_invalid_schema__raises_exception(
      self,
      concrete_parameter_class: Type[PersonClass],
      fixture_name: str,
      invalid_schema: Dict[str, Any],
      request: pytest.FixtureRequest,
  ) -> None:
    parameter_schema = copy.deepcopy(request.getfixturevalue(fixture_name))
    parameter_schema.identifier = invalid_schema
    setattr(
        concrete_parameter_class,
        ParameterValidationMixin.parameter_schema_class_name,
        parameter_schema,
    )

    with pytest.raises(InvalidParameterValidation) as exc:
      concrete_parameter_class(name="string", identifier="string")

    assert_is_invalid_parameter_validation(
        exc=exc,
        description_t=(
            ParameterValidationMixin.
            msg_fmt_parameter_invalid_definition_description,
            "identifier",
        ),
        detail_t=(
            new_line(
                new_line().join(
                    ParameterValidationMixin.
                    msg_fmt_parameter_invalid_definition_detail_tuple
                )
            ),
            (", ".join([value.__name__ for value in TYPES_ALL])),
            (", ".join([value.__name__ for value in TYPES_CONTAINER])),
            *[
                (value + ":").
                ljust(ParameterValidationMixin.parameter_definition_width + 1)
                for value in ParameterValidationMixin.parameter_definition_keys
            ],
        ),
        operation_class=concrete_parameter_class,
    )
