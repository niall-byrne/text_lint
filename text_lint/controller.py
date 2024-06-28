"""Controller class."""

from text_lint.results.forest import ResultForest
from text_lint.schema import Schema
from text_lint.sequencers.rules import RuleSequencer
from text_lint.sequencers.textfile import TextFileSequencer
from text_lint.sequencers.validators import ValidatorSequencer


class Controller:
  """Orchestrates the text file validation process."""

  def __init__(self, file_path: str, schema_path: str) -> None:
    schema = Schema(schema_path)

    self.rules = RuleSequencer(schema)
    self.validators = ValidatorSequencer(schema)

    self.textfile = TextFileSequencer(file_path)
    self.textfile.configure(schema)

    self.forest = ResultForest()

  def start(self) -> None:
    """Start the text file validation process."""
    self.run_rules()
    self.run_validators()

  def run_rules(self) -> None:
    for operation in self.rules:

      try:
        operation.apply(self)
      except StopIteration:
        # TODO: I think an exception should be raised here?
        break
      self.forest.add(operation.results)

  def run_validators(self) -> None:
    for operation in self.validators:
      operation.apply(self)
