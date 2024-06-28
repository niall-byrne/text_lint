"""Test AssertRegexSection class."""

from unittest import mock

import pytest
from text_lint.__helpers__.assertion import (
    assert_assertion_attributes,
    assert_is_assertion_violation,
)
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.results import assert_result_tree
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.exceptions.assertions import AssertionViolation
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.assertions.bases.assertion_regex_base import (
    AssertionRegexBase,
)
from ..assert_regex_section import AssertRegexSection


class TestAssertRegexSection:
  """Test the AssertRegexSection class."""

  def test_initialize__defaults__attributes(self) -> None:
    attributes: AliasOperationAttributes = {
        "hint":
            (
                "one or more adjacent lines (the 'section') "
                "must match this regex"
            ),
        "name": "example assert regex section assertion",
        "operation": "assert_regex_section",
        "regex": "^([a-z-]+):\\s(.+)$",
        "save": None,
        "splits": {},
    }

    instance = AssertRegexSection(
        name="example assert regex section assertion",
        regex="^([a-z-]+):\\s(.+)$",
    )

    assert_assertion_attributes(instance, attributes)

  def test_initialize__defined__attributes(
      self,
      assert_regex_section_instance: AssertRegexSection,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint":
            (
                "one or more adjacent lines (the 'section') "
                "must match this regex"
            ),
        "name": "example assert regex section assertion",
        "operation": "assert_regex_section",
        "regex": "^([a-z-]+):\\s(.+)$",
        "save": "example",
        "splits": {
            2: None
        },
    }

    assert_assertion_attributes(assert_regex_section_instance, attributes)

  def test_initialize__translations(
      self,
      assert_regex_section_instance: AssertRegexSection,
  ) -> None:
    assert_is_translated(assert_regex_section_instance.hint)

  def test_initialize__inheritance(
      self,
      assert_regex_section_instance: AssertRegexSection,
  ) -> None:
    assert_operation_inheritance(
        assert_regex_section_instance,
        bases=(
            AssertionBase,
            AssertionRegexBase,
            AssertRegexSection,
        )
    )

  def test_apply__one_line__matches__stores_result(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.__iter__.return_value = [
        "matching: string",
        "",
    ]

    assert_regex_section_instance.apply(mocked_controller)

    assert len(mocked_controller.forest.add.mock_calls) == 1
    result_tree = mocked_controller.forest.add.mock_calls[0].args[0]
    assert_result_tree(
        result_tree,
        assert_regex_section_instance.save,
        ["matching"],
    )

  def test_apply__two_line__matches__stores_result(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.__iter__.return_value = [
        "matching-one: string1",
        "matching-two: string2",
        "",
    ]

    assert_regex_section_instance.apply(mocked_controller)

    assert len(mocked_controller.forest.add.mock_calls) == 1
    result_tree = mocked_controller.forest.add.mock_calls[0].args[0]
    assert_result_tree(
        result_tree,
        assert_regex_section_instance.save,
        ["matching-one", "matching-two"],
    )
    assert_result_tree(
        result_tree.children[0],
        "matching-one",
        ["string1".split()],
    )
    assert_result_tree(
        result_tree.children[1],
        "matching-two",
        ["string2".split()],
    )

  def test_apply__entire_file__matches__stores_result(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.__iter__.return_value = [
        "matching-one: string1",
        "matching-two: string2",
        "matching-three: string3",
    ]

    assert_regex_section_instance.apply(mocked_controller)

    assert len(mocked_controller.forest.add.mock_calls) == 1
    result_tree = mocked_controller.forest.add.mock_calls[0].args[0]
    assert_result_tree(
        result_tree,
        assert_regex_section_instance.save,
        ["matching-one", "matching-two", "matching-three"],
    )
    assert_result_tree(
        result_tree.children[0],
        "matching-one",
        ["string1".split()],
    )
    assert_result_tree(
        result_tree.children[1],
        "matching-two",
        ["string2".split()],
    )
    assert_result_tree(
        result_tree.children[2],
        "matching-three",
        ["string3".split()],
    )

  def test_apply__two_lines__one_matches__one_does_not_match__stores_result(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.__iter__.return_value = [
        "matching-one: string1",
        "matching2: string",
        "",
    ]

    assert_regex_section_instance.apply(mocked_controller)

    assert len(mocked_controller.forest.add.mock_calls) == 1
    result_tree = mocked_controller.forest.add.mock_calls[0].args[0]
    assert_result_tree(
        result_tree,
        assert_regex_section_instance.save,
        ["matching-one"],
    )
    assert_result_tree(
        result_tree.children[0],
        "matching-one",
        ["string1".split()],
    )

  def test_apply__two_lines__one_matches__one_does_not_match__adjusts_index(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.index = 2
    mocked_textfile.__iter__.return_value = [
        "matching-one: string",
        "matching2: string",
        "",
    ]

    assert_regex_section_instance.apply(mocked_controller)

    assert mocked_textfile.index == 1

  def test_apply__two_lines__no_matches__raises_exception(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_controller: mock.Mock,
      mocked_textfile: mock.MagicMock,
  ) -> None:
    mocked_textfile.index = 1
    mocked_textfile.__iter__.return_value = [
        "matching1: string",
        "matching2: string",
        "",
    ]

    with pytest.raises(AssertionViolation) as exc:
      assert_regex_section_instance.apply(mocked_controller)

    mocked_controller.forest.add.assert_not_called()
    assert_is_assertion_violation(
        exc=exc,
        assertion=assert_regex_section_instance,
        textfile=mocked_textfile,
        expected=assert_regex_section_instance.regex.pattern,
    )
