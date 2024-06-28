"""Shared results testing helpers"""

from typing import TYPE_CHECKING, Any, List, Optional

import pytest
from text_lint.__helpers__.translations import assert_all_translated
from text_lint.exceptions.results import ResultDoesNotExist
from text_lint.results.tree import ResultTree
from text_lint.utilities.translations import f as translation_f
from text_lint.utilities.whitespace import make_visible

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.validators.args.result_set import ResultSet
  from text_lint.results.tree import AliasTreeValue


def assert_is_result_does_not_exist(
    exc: pytest.ExceptionInfo[ResultDoesNotExist],
    result_set: "ResultSet",
    requesting_operation_name: str,
    hint: str,
) -> None:
  expected_translation = []

  def f(*args: Any, nl: int = 0, **kwargs: Any) -> str:
    expected_translation.append(args[0])
    return translation_f(*args, nl=nl, **kwargs)

  message = f(
      ResultDoesNotExist.msg_fmt_does_not_exist,
      nl=1,
  )
  message += f(
      ResultDoesNotExist.msg_fmt_result_source,
      make_visible(result_set.source),
      nl=1,
  )
  message += f(
      ResultDoesNotExist.msg_fmt_schema_operation_name,
      requesting_operation_name,
      nl=1,
  )
  message += f(
      ResultDoesNotExist.msg_fmt_lookup_definition,
      nl=1,
  )
  message += f(
      ResultDoesNotExist.msg_fmt_lookup_result_source,
      make_visible(result_set.source),
      nl=1,
  )
  message += f(
      ResultDoesNotExist.msg_fmt_lookups,
      make_visible(result_set.lookups),
      nl=1,
  )
  message += f(
      ResultDoesNotExist.msg_fmt_hint,
      hint,
      nl=1,
  )

  assert exc.value.__class__ == ResultDoesNotExist
  assert exc.value.args[0] == message
  assert_all_translated(expected_translation)


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
