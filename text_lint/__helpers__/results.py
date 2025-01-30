"""Shared results testing helpers"""

from typing import TYPE_CHECKING, List, Optional

import pytest
from text_lint.__helpers__.translations import TranslationsCapture
from text_lint.exceptions.results import ResultDoesNotExist
from text_lint.results.tree import ResultTree
from text_lint.utilities.whitespace import make_visible

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.validators.args.lookup_expression import (
      LookupExpression,
  )
  from text_lint.results.tree import AliasTreeValue


def assert_is_result_does_not_exist(
    exc: pytest.ExceptionInfo[ResultDoesNotExist],
    lookup_expression: "LookupExpression",
    requesting_operation_name: str,
    hint: str,
) -> None:
  captured = TranslationsCapture()

  message = captured.f(
      ResultDoesNotExist.msg_fmt_does_not_exist,
      nl=1,
  )
  message += captured.f(
      ResultDoesNotExist.msg_fmt_result_source,
      make_visible(lookup_expression.source),
      nl=1,
  )
  message += captured.f(
      ResultDoesNotExist.msg_fmt_schema_operation_name,
      requesting_operation_name,
      nl=1,
  )
  message += captured.f(
      ResultDoesNotExist.msg_fmt_lookup_definition,
      nl=1,
  )
  message += captured.f(
      ResultDoesNotExist.msg_fmt_lookup_result_source,
      make_visible(lookup_expression.source),
      nl=1,
  )
  message += captured.f(
      ResultDoesNotExist.msg_fmt_lookups,
      make_visible(
          [parsed_lookup.name for parsed_lookup in lookup_expression.lookups]
      ),
      nl=1,
  )
  message += captured.f(
      ResultDoesNotExist.msg_fmt_hint,
      hint,
      nl=1,
  )

  assert exc.value.__class__ == ResultDoesNotExist
  assert exc.value.args[0] == message
  captured.assert_all_translated()


def assert_result_tree(
    tree: ResultTree,
    value: Optional["AliasTreeValue"],
    child_values: List["AliasTreeValue"],
) -> None:
  assert isinstance(tree, ResultTree)
  assert tree.value == value
  assert len(tree.children) == len(child_values)
  for child_index, child in enumerate(tree.children):
    assert isinstance(child, ResultTree)
    assert child.value == child_values[child_index]
