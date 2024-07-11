"""Assertion sequence integration testing."""

from typing import TYPE_CHECKING, Callable, List
from unittest import mock

from text_lint.config import NEW_LINE
from text_lint.operations.assertions import (
    AssertBlank,
    AssertEqual,
    AssertSequenceBegins,
    AssertSequenceEnds,
)

if TYPE_CHECKING:
  from text_lint.operations.assertions.bases.assertion_base import (
      AssertionBase,
  )


class TestAssertionSequences:
  """Assertion sequence integration testing."""

  data_valid = (NEW_LINE + "a" + NEW_LINE) * 10

  def test_simple_sequence__correct_assertion_sequence(
      self,
      create_mocked_linter: Callable[[str, str], mock.Mock],
      yaml_simple_sequence: str,
  ) -> None:
    expected_assertions = [AssertSequenceBegins.operation]
    expected_assertions += [
        AssertBlank.operation, AssertEqual.operation,
        AssertSequenceEnds.operation
    ] * 10
    expected_assertions += [AssertSequenceEnds.operation]
    processed_assertions: List["AssertionBase"] = []
    linter = create_mocked_linter(yaml_simple_sequence, self.data_valid)

    for assertion in linter.assertions:
      assertion.apply(linter.state.assertion())
      processed_assertions.append(assertion)

    assert len(processed_assertions) == len(expected_assertions)
    for processed_assertion, expected_assertion in zip(
        processed_assertions,
        expected_assertions,
    ):
      assert processed_assertion.operation == expected_assertion

  def test_nested_sequence__correct_assertion_sequence(
      self,
      create_mocked_linter: Callable[[str, str], mock.Mock],
      yaml_nested_sequence: str,
  ) -> None:
    expected_assertions = [AssertSequenceBegins.operation]
    expected_assertions += [
        AssertSequenceBegins.operation, AssertBlank.operation,
        AssertEqual.operation, AssertSequenceEnds.operation,
        AssertSequenceEnds.operation
    ] * 10
    expected_assertions += [AssertSequenceEnds.operation]
    processed_assertions: List["AssertionBase"] = []
    linter = create_mocked_linter(yaml_nested_sequence, self.data_valid)

    for assertion in linter.assertions:
      assertion.apply(linter.state.assertion())
      processed_assertions.append(assertion)

    assert len(processed_assertions) == len(expected_assertions)
    for processed_assertion, expected_assertion in zip(
        processed_assertions,
        expected_assertions,
    ):
      assert processed_assertion.operation == expected_assertion

  def test_infinite_sequence__correct_assertion_sequence(
      self,
      create_mocked_linter: Callable[[str, str], mock.Mock],
      yaml_infinite_sequence: str,
  ) -> None:
    expected_assertions = [AssertSequenceBegins.operation]
    expected_assertions += [
        AssertBlank.operation, AssertEqual.operation,
        AssertSequenceEnds.operation
    ] * 10
    processed_assertions: List["AssertionBase"] = []
    linter = create_mocked_linter(yaml_infinite_sequence, self.data_valid)

    while True:
      try:
        assertion = next(linter.assertions)
        assertion.apply(linter.state.assertion())
        processed_assertions.append(assertion)
      except StopIteration:
        break

    assert len(processed_assertions) == len(expected_assertions)
    for processed_assertion, expected_assertion in zip(
        processed_assertions, expected_assertions
    ):
      assert processed_assertion.operation == expected_assertion
