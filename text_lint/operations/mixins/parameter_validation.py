"""ParameterValidationMixin class."""

from typing import Any, Callable, Dict, Tuple, Type, Union

from text_lint.exceptions.operations import InvalidParameterValidation
from text_lint.utilities.translations import _

AliasParameterValidator = Union[
    None,
    Type[Any],
    Callable[[str], bool],
    Tuple[Type[Any], "AliasParameterValidator"],
]
AliasParameterSchema = Dict[str, AliasParameterValidator]


class ParameterValidationMixin:
  """A mixin class to validate constructor parameters."""

  parameters: AliasParameterSchema

  msg_fmt_parameter_invalid_value = _(
      "The value '{0}' is not valid for parameter '{1}'"
  )
  msg_fmt_parameter_invalid_container_description = _(
      "Complex types must be containers."
  )
  msg_fmt_parameter_invalid_container_detail = _(
      "The parameter '{0}' specifies type '{1}' which is not a container type."
  )
  msg_fmt_parameter_invalid_dictionary_definition_description = _(
      "Complex dictionaries are declared as tuples of key/value pairs."
  )
  msg_fmt_parameter_invalid_dictionary_definition_detail = _(
      "The parameter '{0}' specifies type '{1}' which is not a tuple of "
      "key/value pairs."
  )

  def __post_init__(self) -> None:
    for attribute_name, parameter_validator in self.parameters.items():
      attribute = getattr(self, attribute_name)
      self.__validate_attribute__(
          attribute, attribute_name, parameter_validator
      )

  def __validate_attribute__(
      self,
      attribute: Any,
      attribute_name: str,
      parameter_validator: AliasParameterValidator,
  ) -> bool:
    if parameter_validator is None:
      if attribute is None:
        return True
    elif isinstance(parameter_validator, type):
      if isinstance(attribute, parameter_validator):
        return True
    elif isinstance(parameter_validator, tuple):
      if self.__validate_complex_attribute__(
          *parameter_validator,
          attribute,
          attribute_name,
      ):
        return True
    elif callable(parameter_validator):
      if parameter_validator(attribute):
        return True

    raise TypeError(
        self.msg_fmt_parameter_invalid_value.format(
            attribute,
            attribute_name,
        )
    )

  def __validate_complex_attribute__(
      self,
      container_type: Type[Any],
      expected_type: Any,
      attribute: Any,
      attribute_name: Any,
  ) -> bool:

    if container_type in (list, tuple):
      return all(
          self.__validate_attribute__(
              element,
              attribute_name,
              expected_type,
          ) for element in attribute
      )

    if container_type == dict:
      if not isinstance(expected_type, tuple) or len(expected_type) != 2:
        raise InvalidParameterValidation(
            translated_description=self.
            msg_fmt_parameter_invalid_dictionary_definition_description,
            translated_detail=self.
            msg_fmt_parameter_invalid_dictionary_definition_detail.format(
                attribute_name,
                expected_type,
            ),
            operation_class=self.__class__,
        )

      return all(
          self.__validate_attribute__(
              nested_key,
              attribute_name,
              expected_type[0],
          ) and self.__validate_attribute__(
              nested_value,
              attribute_name,
              expected_type[1],
          ) for nested_key, nested_value in attribute.items()
      )

    raise InvalidParameterValidation(
        translated_description=self.
        msg_fmt_parameter_invalid_container_description,
        translated_detail=self.msg_fmt_parameter_invalid_container_detail.
        format(
            attribute_name,
            container_type,
        ),
        operation_class=self.__class__,
    )
