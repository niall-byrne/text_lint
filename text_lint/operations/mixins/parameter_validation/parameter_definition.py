"""ParameterDefinition class."""

from typing import Any, Type

from .constants import (
    TYPES_ALL,
    TYPES_CONTAINER,
    AliasParameterOfType,
    AliasParameterValidator,
)


class ParameterDefinition:
  """Encapsulate a class attribute with validation constraints."""

  # pylint: disable=too-many-arguments,too-many-positional-arguments
  def __init__(
      self,
      attribute: Any,
      attribute_name: str,
      expected_type: Type[Any],
      optional: bool = False,
      of: AliasParameterOfType = None,
      validators: AliasParameterValidator = ()
  ) -> None:
    """Instantiate ParameterDefinition instances.

    :param attribute: The value of the attribute being encapsulated.
    :param attribute_name: The name of the attribute being encapsulated.
    :param expected_type: The type the attribute should conform to.
    :param optional: A boolean which allows the attribute to be optional.
    :param of: Required for container types, defines the nested value types.
    :param validators: A tuple of validator functions for this attribute.
    """
    assert isinstance(attribute_name, str)
    assert isinstance(optional, bool)
    assert expected_type in TYPES_ALL
    if of:
      assert expected_type in TYPES_CONTAINER
      if expected_type == dict:
        assert isinstance(of, tuple)
        assert len(of) == 2
      if expected_type in (list, tuple):
        assert isinstance(of, type)
    assert isinstance(validators, (list, tuple))
    assert all(callable(validator) for validator in validators)

    self.attribute = attribute
    self.attribute_name = attribute_name
    self.expected_type = expected_type
    self.optional = optional
    self.of = of
    self.validators = validators
