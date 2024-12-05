"""ValidateExpression class."""

from typing import TYPE_CHECKING, Union

from text_lint.config import SAVED_NAME_REGEX
from text_lint.operations.bases.operation_base import YAML_EXAMPLE_SECTIONS
from text_lint.operations.mixins.parameter_validation import (
    validator_factories,
)
from text_lint.operations.validators.bases.validator_comparison_base import (
    ValidationComparisonBase,
)
from text_lint.operations.validators.expressions import expressions_registry
from text_lint.results.tree import ResultTree
from text_lint.utilities.translations import _

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import ValidatorState
  from text_lint.operations.validators.args.lookup_expression import (
      AliasYamlLookupExpressionSet,
  )
  from text_lint.results.forest import AliasLookupResult


YAML_EXAMPLE_COMPONENTS = (
    _("expression validator example"),
)
YAML_EXAMPLE = """

- name: {0}
  operation: validate_expression
  operator: "+"
  saved_a:
    - source1.capture(1).to_count()
  saved_b:
    - ~10
  new_saved: expression_result

{notes_section}:
  - Valid operators are: {valid_operators}

""".format(
    *YAML_EXAMPLE_COMPONENTS,
    **YAML_EXAMPLE_SECTIONS,
    valid_operators=" ".join(expressions_registry.keys()),
)


class ValidateExpression(ValidationComparisonBase):
  """A validator to combine result lookups into a new save id."""

  hint = _("perform math on save ids to create a new save id")
  operation = "validate_expression"
  yaml_example = YAML_EXAMPLE

  msg_fmt_comparison_failure = _("'{0}' {2} '{1}'")
  msg_fmt_comparison_success = _("EXPRESSION: '{0}' {2} '{1}'")
  msg_fmt_invalid_comparison_description = _(
      "Cannot perform operation: '{0}' {2} '{1}'"
  )
  msg_fmt_invalid_comparison_detail = _(
      "Cannot convert both '{0}' and '{1}' to numeric values."
  )

  def __init__(
      self,
      name: str,
      new_saved: str,
      operator: str,
      saved_a: "AliasYamlLookupExpressionSet",
      saved_b: "AliasYamlLookupExpressionSet",
  ) -> None:
    """Initialize ValidateExpression instances.

    :param name: The configured name of this validator.
    :param new_saved: The new saved id to create.
    :param operator: An operator applied to the lookup expression result pairs.
    :param saved_a: A list of YAML lookup expressions to evaluate.
    :param saved_b: A second list of YAML lookup expressions to evaluate.
    :raises: TypeError
    """
    self.new_saved = new_saved
    self.operator = operator
    super().__init__(name, saved_a, saved_b)
    self.new_tree = ResultTree.create(value=new_saved)
    self.msg_fmt_comparison_failure = self.msg_fmt_comparison_failure.replace(
        "{2}",
        self.operator,
    )
    self.msg_fmt_comparison_success = self.msg_fmt_comparison_success.replace(
        "{2}",
        self.operator,
    )
    self.msg_fmt_invalid_comparison_description = (
        self.msg_fmt_invalid_comparison_description.replace(
            "{2}",
            self.operator,
        )
    )

  class Parameters(ValidationComparisonBase.Parameters):
    """Parameter validation for this operation."""

    # pylint: disable=duplicate-code
    new_saved = {
        "type":
            str,
        "validators":
            [validator_factories.create_matches_regex(SAVED_NAME_REGEX)],
    }
    operator = {
        "type":
            str,
        "validators":
            [
                validator_factories.create_is_in(
                    tuple(expressions_registry.keys())
                )
            ],
    }

  def apply(self, state: "ValidatorState") -> None:
    """Apply the ValidateCombine validator logic."""
    super().apply(state)

    state.save(self.new_tree)

  def comparison(
      self,
      result_a: "AliasLookupResult",
      result_b: "AliasLookupResult",
  ) -> bool:
    """Apply the operator to each pair of lookup expression results.

    A new result tree will be created with the expression result.

    :param result_a: A lookup expression result to operate on.
    :param result_b: A second lookup expression result to operate on.
    :returns: Whether the operation could be applied to the result pair.
    :raises: TypeError (which is handled by the base class)
    """
    try:
      float_a = float(result_a)  # type: ignore[arg-type]
      float_b = float(result_b)  # type: ignore[arg-type]
    except ValueError as exc:
      raise TypeError from exc

    expression_class = expressions_registry[self.operator]
    result = expression_class().apply(float_a, float_b)

    self._create_children(result)

    if isinstance(result, bool):
      return result

    return True

  def _create_children(
      self,
      value: Union[bool, float],
  ) -> None:
    instance = ResultTree.create(value=str(value))
    self.new_tree.children.append(instance)
