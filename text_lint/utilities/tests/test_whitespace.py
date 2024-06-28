"""Test the whitespace utilities."""

from text_lint import config
from .. import whitespace


class TestMakeVisible:
  """Test the make_visible function."""

  def test_new_lines__returns_correct_value(self) -> None:
    received_string = whitespace.make_visible("string \n")

    assert received_string == "string \\n"

  def test_tabs__returns_correct_value(self) -> None:
    received_string = whitespace.make_visible("string \t")

    assert received_string == "string \\t"

  def test_carriage_return__returns_correct_value(self) -> None:
    received_string = whitespace.make_visible("string \r")

    assert received_string == "string \\r"


class TestNewLine:
  """Test the new_line function."""

  def test_defaults__returns_correct_value(self) -> None:
    received_string = whitespace.new_line()

    assert received_string == config.NEW_LINE

  def test_specified_string__returns_correct_value(self) -> None:
    received_string = whitespace.new_line("string")

    assert received_string == "string" + config.NEW_LINE

  def test_integer__returns_correct_value(self) -> None:
    received_string = whitespace.new_line(1)

    assert received_string == str(1) + config.NEW_LINE
