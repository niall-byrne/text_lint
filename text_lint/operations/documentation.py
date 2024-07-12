"""OperationDocumentation class."""

import sys
from typing import TYPE_CHECKING, List, Mapping, Tuple, Type

from text_lint.config import NEW_LINE
from text_lint.operations.assertions import assertion_registry
from text_lint.operations.lookups import lookup_registry
from text_lint.operations.validators import validator_registry
from text_lint.utilities.translations import _, f

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any

  from text_lint.operations.bases.operation_base import OperationBase

AliasRegistry = Mapping[str, Type["OperationBase[Any]"]]


class OperationDocumentation:
  """Documentation for text file Operation subclasses."""

  content = ""
  registries: Mapping[str, AliasRegistry]

  msg_fmt_operation_list_headers = [
      _("Schema Operation List"),
      _("Type: '{0}'"),
  ]
  msg_fmt_operation_doc_headers = [
      _("Operation: '{0}'"),
      _("Type:      '{0}'"),
      _("Purpose:   '{0}'"),
      _("Example: {0}"),
  ]
  msg_fmt_operation_unknown = _("Unknown operation '{0}' !")

  def __init__(self) -> None:
    self.registries = {
        "Assertion": self._filter_registry(assertion_registry),
        "Validator": self._filter_registry(validator_registry),
        "Validator Lookup": self._filter_registry(lookup_registry),
    }

  def _filter_registry(self, registry: AliasRegistry) -> AliasRegistry:
    return {
        operation_name: operation_class
        for (operation_name, operation_class) in registry.items()
        if not operation_class.internal_use_only
    }

  def list(self) -> None:
    """Generate a list of all operations in the registries."""

    self.content += f(
        self.msg_fmt_operation_list_headers[0],
        nl=1,
    )
    self.content += "-" * (len(self.content) - 1) + NEW_LINE * 2

    for registry_name, registry in self.registries.items():
      self.content += f(
          self.msg_fmt_operation_list_headers[1],
          registry_name,
          nl=1,
      )
      for operation in sorted(registry):
        self.content += "".join(
            [
                "  ",
                operation.ljust(24),
                registry[operation].hint,
                NEW_LINE,
            ]
        )
      self.content += NEW_LINE

  def search(self, operation_name: str) -> None:
    """Search the documentation for the specified operation name."""

    for registry_type, registry in self.registries.items():
      current_registry = dict(registry)
      if operation_name in current_registry:
        self._create_operation_documentation_content(
            current_registry[operation_name],
            registry_type,
        )
        break
    else:
      self.content += f(
          self.msg_fmt_operation_unknown,
          operation_name,
      )

  def _create_operation_documentation_content(
      self,
      operation_class: Type["OperationBase[Any]"],
      registry_type: str,
  ) -> None:
    fmt_contents: List[Tuple[str, int]] = [
        (operation_class.operation, 1),
        (registry_type, 1),
        (operation_class.hint, 1),
        (operation_class.yaml_example, 0),
    ]

    for msg_fmt, fmt_content in zip(
        self.msg_fmt_operation_doc_headers,
        fmt_contents,
    ):
      self.content += f(msg_fmt, fmt_content[0], nl=fmt_content[1])

  def print(self) -> None:
    """Write the search results to the console."""

    sys.stdout.write(self.content + NEW_LINE)
