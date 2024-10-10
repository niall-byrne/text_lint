"""ParameterValidationMixin class."""

from typing import Any, Callable, Dict, Tuple, Type, Union, Optional

from text_lint.exceptions.operations import InvalidParameterValidation
from text_lint.utilities.translations import _

AliasParameterValidator = Union[
    Type[Any],
    Callable[[str], bool],
    Tuple[Type[Any], "AliasParameterValidator"],
]
AliasParameterSchema = Dict[str, AliasParameterValidator]


class ParameterDefinition:
  """Container for parsed schema parameters."""

  def __init__(
      self,
      attribute: Any,
      attribute_name: str,
      expected_type: AliasParameterValidator,
      optional: bool = False,
      of: Optional[Tuple[Type[Any], "AliasParameterValidator"]] = None,
  ):
    assert isinstance(attribute_name, str)
    assert isinstance(optional, bool)
    if of:
      if isinstance(expected_type, dict):
        assert isinstance(of, tuple)
        assert len(of) == 2
      if isinstance(expected_type, list):
        assert isinstance(of, type)

    self.attribute = attribute
    self.attribute_name = attribute_name
    self.expected_type = expected_type
    self.optional = optional
    self.of = of


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
    parameter_schema = getattr(self, "Schema", None)
    if parameter_schema:
      for attribute_name in filter(
          lambda name: not name.startswith('__'),
          dir(parameter_schema),
      ):
        parameter_definition = self.__parse_schema_definition__(attribute_name)
        self.__validate_attribute__(parameter_definition)

  def __parse_schema_definition__(self, attribute_name: str) -> ParameterDefinition:
    try:
      attribute = getattr(self, attribute_name)
      schema_definition = getattr(getattr(self, "Schema"), attribute_name)
      schema_definition["expected_type"] = schema_definition["type"]
      del schema_definition["type"]
      return ParameterDefinition(
        attribute=attribute,
        attribute_name=attribute_name,
        **schema_definition,
      )
    except (KeyError, TypeError, AssertionError):
      raise Exception("very bad")

  def __validate_attribute__(
      self,
      definition: ParameterDefinition,
  ) -> bool:

    if definition.optional is True:
      if definition.attribute is None:
        return True

    if isinstance(definition.expected_type, type):
      if isinstance(definition.attribute, definition.expected_type):
        if definition.expected_type in (dict, list, tuple):
          if self.__validate_complex_attribute__(definition):
            return True
        else:
          return True

    raise TypeError(
        self.msg_fmt_parameter_invalid_value.format(
            definition.attribute,
            definition.attribute_name,
        )
    )

  def __validate_complex_attribute__(
      self,
      definition: ParameterDefinition,
  ) -> bool:

    if definition.expected_type in (list, tuple):
      if definition.of:
        return all(
            self.__validate_attribute__(
                ParameterDefinition(
                  attribute=nested_attribute,
                  attribute_name=definition.attribute_name,
                  expected_type=definition.of,
                )
            ) for nested_attribute in definition.attribute
        )
      else:
        return True

    if definition.expected_type == dict:
      if definition.of:
        return all(
          self.__validate_attribute__(
            ParameterDefinition(
              attribute=nested_key,
              attribute_name=definition.attribute_name,
              expected_type=definition.of[0],
            )
          ) and self.__validate_attribute__(
            ParameterDefinition(
              attribute=nested_value,
              attribute_name=definition.attribute_name,
              expected_type=definition.of[1],
            )
          ) for nested_key, nested_value in definition.attribute.items()
        )
      else:
        return True

    raise InvalidParameterValidation(
        translated_description=self.
        msg_fmt_parameter_invalid_container_description,
        translated_detail=self.msg_fmt_parameter_invalid_container_detail.
        format(
            definition.attribute_name,
            definition.expected_type,
        ),
        operation_class=self.__class__,
    )
