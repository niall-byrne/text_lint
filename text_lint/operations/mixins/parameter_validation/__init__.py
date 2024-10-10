"""ParameterValidationMixin class."""

from typing import Any, Type, cast

from text_lint.exceptions.operations import InvalidParameterValidation
from text_lint.utilities.translations import _
from text_lint.utilities.whitespace import new_line
from .constants import (
    TYPES_ALL,
    TYPES_CONTAINER,
    TYPES_NUMERIC,
    AliasParameterOfType,
    AliasParameterValidator,
)
from .parameter_definition import ParameterDefinition


class ParameterValidationMixin:
  """A mixin class to validate constructor parameters."""

  parameter_definition_keys = ("type", "of", "optional", "validators")
  parameter_definition_width = len(max(parameter_definition_keys, key=len))
  parameter_schema_class_name = "Parameters"

  msg_fmt_parameter_invalid_value = _(
      "The value '{0}' is not valid for parameter '{1}'"
  )
  msg_fmt_parameter_invalid_definition_description = _(
      "The typing schema for parameter '{0}' is invalid."
  )
  msg_fmt_parameter_invalid_definition_detail_tuple = (
      _("Valid parameter definitions must take the form of a dictionary:"),
      _("    {2} specifies the expected python type."),
      _("                supported types: {0}."),
      _("    {3} optional type used only with the container types."),
      _("                container types: {1}."),
      _(
          "                (dicts should specify a tuple of types in "
          "(key, value) format.)"
      ),
      _("    {4} optional bool to accept 'None' as a valid value."),
      _("    {5} optional list of validator functions."),
  )

  def validate_parameters(self) -> None:
    parameter_schema = getattr(self, self.parameter_schema_class_name, None)
    if parameter_schema:
      for attribute_name in filter(
          lambda name: not name.startswith('_'),
          dir(parameter_schema),
      ):
        definition = self.__parse_parameter_definition__(attribute_name)
        self.__validate_attribute__(definition)

  def __parse_parameter_definition__(
      self, attribute_name: str
  ) -> ParameterDefinition:
    attribute = getattr(self, attribute_name)
    schema_definition = dict(
        getattr(
            getattr(
                self,
                self.parameter_schema_class_name,
            ), attribute_name
        )
    )
    try:
      return ParameterDefinition(
          attribute=attribute,
          attribute_name=attribute_name,
          expected_type=schema_definition.pop(
              self.parameter_definition_keys[0]
          ),
          **schema_definition,
      )
    except (KeyError, TypeError, AssertionError) as exc:
      raise InvalidParameterValidation(
          translated_description=self.
          msg_fmt_parameter_invalid_definition_description.
          format(attribute_name),
          translated_detail=new_line(
              new_line().join(
                  self.msg_fmt_parameter_invalid_definition_detail_tuple
              ).format(
                  (", ".join([value.__name__ for value in TYPES_ALL])),
                  (", ".join([value.__name__ for value in TYPES_CONTAINER])),
                  *[
                      (value + ":").ljust(self.parameter_definition_width + 1)
                      for value in self.parameter_definition_keys
                  ],
              )
          ),
          operation_class=self.__class__,
      ) from exc

  def __validate_attribute__(
      self,
      definition: ParameterDefinition,
  ) -> None:

    if definition.optional is False:
      if definition.attribute is None:
        self.__raise_type_error__(definition)

    if definition.expected_type in TYPES_NUMERIC:
      self.__validate_numeric_attribute__(definition)

    if (
        definition.attribute is not None
        and not isinstance(definition.attribute, definition.expected_type)
    ):
      self.__raise_type_error__(definition)

    if definition.expected_type in TYPES_CONTAINER:
      self.__validate_container_attribute__(definition)

    if definition.attribute is not None:
      for validator in definition.validators:
        if not validator(definition.attribute):
          self.__raise_type_error__(definition)

  def __validate_container_attribute__(
      self,
      definition: ParameterDefinition,
  ) -> None:
    if isinstance(definition.attribute, dict):
      self.__validate_dict_attribute__(definition)
    else:
      self.__validate_iterable_attribute__(definition)

  def __validate_dict_attribute__(
      self,
      definition: ParameterDefinition,
  ) -> None:
    if definition.of and isinstance(definition.of, tuple):
      for nested_key, nested_value in definition.attribute.items():
        self.__validate_attribute__(
            ParameterDefinition(
                attribute=nested_key,
                attribute_name=definition.attribute_name,
                expected_type=definition.of[0],
            )
        )
        self.__validate_attribute__(
            ParameterDefinition(
                attribute=nested_value,
                attribute_name=definition.attribute_name,
                expected_type=cast(Type[Any], definition.of[1]),
            )
        )

  def __validate_iterable_attribute__(
      self,
      definition: ParameterDefinition,
  ) -> None:
    if definition.of and isinstance(definition.of, type):
      for nested_attribute in definition.attribute:
        self.__validate_attribute__(
            ParameterDefinition(
                attribute=nested_attribute,
                attribute_name=definition.attribute_name,
                expected_type=definition.of,
            )
        )

  def __validate_numeric_attribute__(
      self,
      definition: ParameterDefinition,
  ) -> None:
    if not isinstance(definition.attribute, (int, float)):
      self.__raise_type_error__(definition)

    casted_value = definition.expected_type(definition.attribute)

    if casted_value != definition.attribute:
      self.__raise_type_error__(definition)

    definition.attribute = definition.expected_type(definition.attribute)

  def __raise_type_error__(
      self,
      definition: ParameterDefinition,
  ) -> None:
    raise TypeError(
        self.msg_fmt_parameter_invalid_value.format(
            definition.attribute,
            definition.attribute_name,
        )
    )
