"""Test AssertRegexSection class."""

from unittest import mock

import pytest
from text_lint.__helpers__.assertion import (
    assert_assertion_attributes,
    assert_state_saved,
)
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import (
    assert_is_translated,
    assert_is_translated_yaml_example,
)
from text_lint.operations.assertions.bases.assertion_base import AssertionBase
from text_lint.operations.assertions.bases.assertion_regex_base import (
    AssertionRegexBase,
)
from ..assert_regex_section import (
    YAML_EXAMPLE,
    YAML_EXAMPLE_COMPONENTS,
    AssertRegexSection,
)


class TestAssertRegexSection:
  """Test the AssertRegexSection class."""

  def test_initialize__defaults__attributes(self) -> None:
    attributes: AliasOperationAttributes = {
        "hint":
            (
                "one or more adjacent lines (the 'section') "
                "must match this regex"
            ),
        "internal_use_only": False,
        "name": "example assert regex section assertion",
        "operation": "assert_regex_section",
        "regex": "^([a-z-]+):\\s(.+)$",
        "save": None,
        "splits": {},
        "yaml_example": YAML_EXAMPLE,
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
        "internal_use_only": False,
        "name": "example assert regex section assertion",
        "operation": "assert_regex_section",
        "regex": "^([a-z-]+):\\s(.+)$",
        "save": "example",
        "splits": {
            2: None
        },
        "yaml_example": YAML_EXAMPLE,
    }

    assert_assertion_attributes(assert_regex_section_instance, attributes)

  def test_initialize__translations(
      self,
      assert_regex_section_instance: AssertRegexSection,
  ) -> None:
    assert_is_translated(assert_regex_section_instance.hint)
    assert_is_translated_yaml_example(
        assert_regex_section_instance.yaml_example,
        YAML_EXAMPLE_COMPONENTS,
        assertion_options=True,
    )

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

  def test_apply__one_line__matches__saves_result(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.next.side_effect = [
        "matching: string",
        "",
    ]

    assert_regex_section_instance.apply(mocked_state)

    assert_state_saved(
        assert_regex_section_instance,
        mocked_state,
        ["matching: string"],
    )

  def test_apply__two_line__matches__saves_result(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.next.side_effect = [
        "matching-one: string1",
        "matching-two: string2",
        "",
    ]

    assert_regex_section_instance.apply(mocked_state)

    assert_state_saved(
        assert_regex_section_instance,
        mocked_state,
        [
            "matching-one: string1",
            "matching-two: string2",
        ],
    )

  def test_apply__entire_file__matches__saves_result(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.next.side_effect = [
        "matching-one: string1",
        "matching-two: string2",
        "matching-three: string3",
    ]

    assert_regex_section_instance.apply(mocked_state)

    assert_state_saved(
        assert_regex_section_instance,
        mocked_state,
        [
            "matching-one: string1",
            "matching-two: string2",
            "matching-three: string3",
        ],
    )

  def test_apply__two_lines__one_matches__one_does_not_match__saves_result(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.next.side_effect = [
        "matching-one: string1",
        "matching2: string",
        "",
    ]

    assert_regex_section_instance.apply(mocked_state)

    assert_state_saved(
        assert_regex_section_instance,
        mocked_state,
        [
            "matching-one: string1",
        ],
    )

  def test_apply__two_lines__one_matches__one_does_not_match__calls_rewind(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.next.side_effect = [
        "matching-one: string1",
        "matching2: string",
        "",
    ]

    assert_regex_section_instance.apply(mocked_state)

    mocked_state.rewind.assert_called_once_with()

  def test_apply__two_lines__no_matches__calls_fail(
      self,
      assert_regex_section_instance: AssertRegexSection,
      mocked_state: mock.Mock,
  ) -> None:
    mocked_state.fail.side_effect = Exception
    mocked_state.next.side_effect = [
        "matching1: string",
        "matching2: string",
        "",
    ]

    with pytest.raises(Exception):
      assert_regex_section_instance.apply(mocked_state)

    mocked_state.fail.assert_called_once_with(
        assert_regex_section_instance.regex.pattern
    )
