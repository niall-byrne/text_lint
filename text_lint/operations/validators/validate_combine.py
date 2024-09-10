"""ValidateCombine class."""

from typing import TYPE_CHECKING, List

from text_lint.operations.validators.args.lookup_expression import (
    LookupExpressionSetArg,
)
from text_lint.operations.validators.bases.validator_base import ValidatorBase
from text_lint.results.tree import ResultTree
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import ValidatorState
  from text_lint.operations.validators.args.lookup_expression import (
      AliasYamlLookupExpressionSet,
  )
  from text_lint.results.forest import AliasLookupResult

YAML_EXAMPLE = """

- name: combine validator example
  operation: validate_combine
  saved:
    - source1.capture()
    - source2.capture()
    - ~source3_name
  new_saved: new_source

"""


class ValidateCombine(ValidatorBase):
  """A validator to combine result lookups into a new save id."""

  hint = _("combines a set of lookups into a new save id")
  operation = "validate_combine"
  yaml_example = YAML_EXAMPLE

  msg_fmt_combine = _("COMBINE: '{0}' into '{1}'")

  def __init__(
      self,
      name: str,
      new_saved: str,
      saved: "AliasYamlLookupExpressionSet",
  ):
    super().__init__(name)
    self.new_tree = ResultTree.create(value=new_saved)
    self.saved_results = LookupExpressionSetArg.create(saved)

  def apply(self, state: "ValidatorState") -> None:
    """Apply the ValidateCombine validator logic."""

    for requested_lookup_to_combine in self.saved_results:

      result = state.lookup_expression(requested_lookup_to_combine)
      self._create_children(result, self.new_tree.children)

      state.log(
          f(
              self.msg_fmt_combine,
              requested_lookup_to_combine.name,
              self.new_tree.value,
          ),
          indent=True,
      )

    state.save(self.new_tree)

  def _create_children(
      self,
      result: "AliasLookupResult",
      created: List[ResultTree],
  ) -> None:
    if isinstance(result, str):
      instance = ResultTree.create(value=result)
      created.append(instance)
    else:
      for element in result:
        self._create_children(element, created)
