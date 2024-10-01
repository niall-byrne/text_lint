"""AssertionState class."""

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, List, Match, Sequence, Union

from text_lint.exceptions.assertions import (
    AssertionLogicError,
    AssertionViolation,
)
from text_lint.utilities.translations import _
from .bases.state_base import StateBase

if TYPE_CHECKING:  # no cover
  from text_lint.controller import Controller
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )


class AssertionState(StateBase):
  """State for assertion operations."""

  operation: "AssertionBase"

  msg_fmt_logic_error_rewind = _(
      "An assertion may not rewind the text file twice."
  )

  def __init__(self, linter: "Controller") -> None:
    super().__init__(linter)
    self.rewound = -1
    self.operation = linter.assertions.last

  def loop(self, assertions: List["AssertionBase"], count: int) -> None:
    """Start a looped sequence of assertions after the current operation."""

    self.linter.assertions.start_repeating(count)
    self.linter.assertions.insert(assertions)

  def loop_stop(self) -> None:
    """Stop a looped sequence of assertions."""

    self.linter.assertions.stop_repeating()

  def next(self) -> str:
    """Read the next line from the text file."""

    return next(self.linter.textfile)

  def rewind(self) -> str:
    """Rewind the text file so another assertion can try matching."""

    if self.linter.textfile.index == self.rewound:
      raise AssertionLogicError(
          assertion=self.operation,
          hint=self.msg_fmt_logic_error_rewind,
          textfile=self.linter.textfile,
      )
    self.linter.textfile.index -= 1
    self.rewound = self.linter.textfile.index
    return self.linter.textfile.current

  def save(self, matches: Union[Match[str], Sequence[Match[str]]]) -> None:
    """Save the given regex match group(s)."""

    if self.operation.save and matches:

      if not isinstance(matches, Iterable):
        matches = [matches]

      result_tree = self.operation.create_result_tree(matches)
      self.linter.forest.add(result_tree)

  def fail(self, *args: Any, **kwargs: Any) -> None:
    """Raise an exception indicating this operation has failed."""

    expected = args[0] if args else kwargs["exception"]

    raise AssertionViolation(
        assertion=self.operation,
        expected=expected,
        textfile=self.linter.textfile,
    )
