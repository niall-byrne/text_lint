"""ValidateEqual class."""

from typing import TYPE_CHECKING

from text_lint.operations.validators.bases.validator_comparison_base import (
    ValidationComparisonBase,
)
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.results.forest import AliasLookupResult

YAML_EXAMPLE = """

- name: equality validator example
  operation: validate_equal
  saved_a:
    - source1.capture()
  saved_b:
    - source2.capture()

"""


class ValidateEqual(ValidationComparisonBase):
  """A validator to check equality between result lookups."""

  hint = _("validates equality between sets of values")
  operation = "validate_equal"
  yaml_example = YAML_EXAMPLE

  msg_fmt_comparison_failure = _("'{0}' != '{1}'")
  msg_fmt_comparison_success = _("EQUAL: '{0}' == '{1}'")

  def comparison(
      self,
      result_a: "AliasLookupResult",
      result_b: "AliasLookupResult",
  ) -> bool:
    """Perform the result comparison between each result element."""

    return bool(result_a == result_b)
