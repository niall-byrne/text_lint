"""Controller class."""

from text_lint.exceptions.sequencers import UnconsumedData
from text_lint.results.forest import ResultForest
from text_lint.schema import Schema
from text_lint.sequencers.patterns.loop import LinearLoopPattern
from text_lint.sequencers.rules import RuleSequencer
from text_lint.sequencers.textfile import TextFileSequencer
from text_lint.sequencers.validators import ValidatorSequencer
from text_lint.utilities.translations import _


class Controller:
  """Orchestrates the text file parsing and validation processes."""

  msg_fmt_all_rules_not_read = _(
      "The entire file was read before all schema rules were run."
  )
  msg_fmt_entire_file_not_read = _(
      "The entire file was not read after all schema rules were run."
  )

  def __init__(self, file_path: str, schema_path: str) -> None:
    schema = Schema(schema_path)

    self.rules = RuleSequencer(schema)
    self.validators = ValidatorSequencer(schema)

    self.textfile = TextFileSequencer(file_path)
    self.textfile.configure(schema)

    self.forest = ResultForest()

  def start(self) -> None:
    """Start the text file parsing and validation processes."""

    self._run_rules()
    self._ensure_all_rules()
    self._ensure_eof()
    self._run_validators()

  def _run_rules(self) -> None:
    count = 0
    for operation in self.rules:
      count += 1
      try:
        operation.apply(self)
      except StopIteration:
        # Text file has finished.
        break
      self.forest.add(operation.results)

  def _run_validators(self) -> None:
    for operation in self.validators:
      operation.apply(self)

  def _ensure_all_rules(self) -> None:
    try:
      next(self.rules)
    except StopIteration:
      pass
    else:
      if not isinstance(self.rules.pattern, LinearLoopPattern):
        raise UnconsumedData(self.msg_fmt_all_rules_not_read)

  def _ensure_eof(self) -> None:
    try:
      next(self.textfile)
    except StopIteration:
      pass
    else:
      raise UnconsumedData(self.msg_fmt_entire_file_not_read)
