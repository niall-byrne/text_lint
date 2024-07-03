"""ValidateCombine class."""

from typing import TYPE_CHECKING, List

from text_lint.operations.validators.args.result_set import ResultSetArg
from text_lint.operations.validators.bases.validator_base import ValidationBase
from text_lint.results.tree import ResultTree
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.controller import Controller
  from text_lint.operations.validators.args.result_set import AliasYamlResultSet
  from text_lint.results.forest import AliasLookupResult

YAML_EXAMPLE = """

- name: combine validator example
  operation: validate_combine
  saved:
    - source1.capture
    - source2.capture
    - ~source3_name
  new_saved: new_source

"""


class ValidateCombine(ValidationBase):
  """A validator to combine result lookups into new saved results."""

  hint = _("combines a set of lookups into a new saved result")
  operation = "validate_combine"
  yaml_example = YAML_EXAMPLE

  msg_fmt_combine = _("COMBINE: '{0}' into '{1}'")

  def __init__(
      self,
      name: str,
      new_saved: str,
      saved: "AliasYamlResultSet",
  ):
    super().__init__(name)
    self.new_tree = ResultTree.create(value=new_saved)
    self.saved_results = ResultSetArg.create(saved)

  def apply(self, controller: "Controller") -> None:
    """Apply the ValidateCombine validator logic."""

    for requested_lookup_to_combine in self.saved_results:

      result = controller.forest.lookup(
          controller,
          requested_lookup_to_combine,
          self.name,
      )

      self._create_children(result, self.new_tree.children)

      self.print(
          f(
              self.msg_fmt_combine,
              requested_lookup_to_combine.name,
              self.new_tree.value,
          )
      )

    controller.forest.add(self.new_tree)

  def _create_children(
      self,
      value: "AliasLookupResult",
      created: List[ResultTree],
  ) -> None:
    if isinstance(value, str):
      instance = ResultTree.create(value=value)
      created.append(instance)
    else:
      for element in value:
        self._create_children(element, created)
