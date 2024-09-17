"""ValidateNotEqual class."""

from typing import TYPE_CHECKING

from text_lint.operations.validators.bases.validator_comparison_base import (
    ValidationComparisonBase,
)
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.results.forest import AliasLookupResult

YAML_EXAMPLE_COMPONENTS = (
    _("non-equality validator example"),
)
YAML_EXAMPLE = """

- name: {0}
  operation: validate_not_equal
  saved_a:
    - source1.capture(1)
  saved_b:
    - source2.capture(1)

""".format(*YAML_EXAMPLE_COMPONENTS)


class ValidateNotEqual(ValidationComparisonBase):
  """A validator to check non-equality between result lookups."""

  hint = _("validates non-equality between sets of values")
  operation = "validate_not_equal"
  yaml_example = YAML_EXAMPLE

  msg_fmt_comparison_failure = _("'{0}' == '{1}'")
  msg_fmt_comparison_success = _("NOT EQUAL: '{0}' != '{1}'")

  def comparison(
      self,
      result_a: "AliasLookupResult",
      result_b: "AliasLookupResult",
  ) -> bool:
    """Perform the result comparison between each result element."""

    return result_a != result_b
