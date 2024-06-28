"""Controller class."""

from typing import TYPE_CHECKING

from text_lint.logging import Logger
from text_lint.logging import contexts as logging_contexts
from text_lint.results.forest import ResultForest
from text_lint.schema import Schema
from text_lint.sequencers.assertions import AssertionSequencer
from text_lint.sequencers.textfile import TextFileSequencer
from text_lint.sequencers.validators import ValidatorSequencer

if TYPE_CHECKING:  # no cover
  from text_lint.controller.settings import ControllerSettings


class Controller:
  """Orchestrates the text file validation process."""

  def __init__(self, settings: "ControllerSettings") -> None:
    self.settings = settings

    schema = Schema(self.settings.schema_path)

    self.assertions = AssertionSequencer(schema)
    self.validators = ValidatorSequencer(schema)

    self.textfile = TextFileSequencer(self.settings.file_path)
    self.textfile.configure(schema)

    self.forest = ResultForest()

    self.log = Logger(self)

  def start(self) -> None:
    """Start the text file validation process."""
    with logging_contexts.main(self):
      with logging_contexts.assertion_section(self):
        self.run_assertions()
      with logging_contexts.validator_section(self):
        self.run_validators()

  def run_assertions(self) -> None:
    for operation in self.assertions:

      try:
        with logging_contexts.assertion(self, operation):
          operation.apply(self)
      except StopIteration:
        # TODO: I think an exception should be raised here?
        break

  def run_validators(self) -> None:
    for operation in self.validators:
      with logging_contexts.validator(self, operation):
        operation.apply(self)
