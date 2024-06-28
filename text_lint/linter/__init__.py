"""Linter class."""

from typing import TYPE_CHECKING

from text_lint.linter import states
from text_lint.linter.logging import Logger
from text_lint.linter.logging import contexts as logging_contexts
from text_lint.results.forest import ResultForest
from text_lint.schema import Schema
from text_lint.sequencers.assertions import AssertionSequencer
from text_lint.sequencers.textfile import TextFileSequencer
from text_lint.sequencers.validators import ValidatorSequencer

if TYPE_CHECKING:  # no cover
  from text_lint.linter.settings import LinterSettings


class Linter:
  """Orchestrates the text file linting process."""

  def __init__(self, settings: "LinterSettings") -> None:
    self.settings = settings

    schema = Schema(self.settings.schema_path)

    self.assertions = AssertionSequencer(schema)
    self.validators = ValidatorSequencer(schema)

    self.textfile = TextFileSequencer(self.settings.file_path)
    self.textfile.configure(schema)

    self.states = states.StateFactory(self)

    self.forest = ResultForest()

    self.log = Logger(self)

  def start(self) -> None:
    """Start the text file linting process."""

    with logging_contexts.main(self):
      with logging_contexts.assertion_section(self):
        self.run_assertions()
      with logging_contexts.validator_section(self):
        self.run_validators()

  def run_assertions(self) -> None:
    for operation in self.assertions:

      try:
        with logging_contexts.assertion(self, operation):
          operation.apply(self.states.assertion())
      except StopIteration:
        # TODO: I think an exception should be raised here?
        break

  def run_validators(self) -> None:
    for operation in self.validators:
      with logging_contexts.validator(self, operation):
        operation.apply(self.states.validator())
