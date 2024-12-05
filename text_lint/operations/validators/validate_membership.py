"""ValidateMembership class."""

from typing import TYPE_CHECKING

from text_lint.operations.validators.bases.validator_comparison_base import (
    ValidationComparisonBase,
)
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.validators.args.lookup_expression import (
      AliasYamlLookupExpressionSet,
  )
  from text_lint.results.forest import AliasLookupResult

YAML_EXAMPLE_COMPONENTS = (
    _("membership validator example"),
)
YAML_EXAMPLE = """

- name: {0}
  operation: validate_membership
  saved_container:
    - source1.capture(1)
  saved_value:
    - source2.capture(1)

""".format(*YAML_EXAMPLE_COMPONENTS)


class ValidateMembership(ValidationComparisonBase):
  """A validator to check if values are found inside a result."""

  hint = _("validates membership of values inside other values")
  operation = "validate_membership"
  yaml_example = YAML_EXAMPLE

  msg_fmt_comparison_failure = _("'{1}' not in '{0}'")
  msg_fmt_comparison_success = _("MEMBERSHIP: '{1}' in '{0}'")
  msg_fmt_invalid_comparison_detail = _(
      "Cannot test for membership of '{1}' in '{0}'"
  )

  def __init__(  # pylint: disable=useless-parent-delegation
      self,
      name: str,
      saved_container: "AliasYamlLookupExpressionSet",
      saved_value: "AliasYamlLookupExpressionSet",
  ) -> None:
    """Initialize ValidateMembership instances.

    :param name: The configured name of this validator.
    :param saved_container: A list of lookup expressions yielding value sets.
    :param saved_value: A list of lookup expressions yielding single values.
    :raises: TypeError
    """
    super().__init__(name, saved_container, saved_value)

  def comparison(
      self,
      result_a: "AliasLookupResult",
      result_b: "AliasLookupResult",
  ) -> bool:
    """Determine if result_b is in the evaluated result_a value set."""
    return result_b in result_a
