"""Shared integration test fixtures."""
# pylint: disable=redefined-outer-name

from io import StringIO
from typing import Callable
from unittest import mock

import pytest
from text_lint.controller import Controller
from text_lint.schema import Schema
from text_lint.sequencers.rules import RuleSequencer
from text_lint.sequencers.textfile import TextFileSequencer

YAML_PREFIX = """
---
version: "0.1.0"

settings:
  comment_regex: "^(#\\\\s|#[^!]).+$"

rules:
"""

YAML_SUFFIX = """
validators: []
"""


@pytest.fixture
def mocked_controller() -> mock.MagicMock:
  return mock.MagicMock()


@pytest.fixture
def mocked_file_content_schema() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_file_content_file() -> StringIO:
  return StringIO()


@pytest.fixture
def mocked_file_handle(
    mocked_file_content_schema: StringIO,
    mocked_file_content_file: StringIO,
) -> mock.MagicMock:
  instance = mock.MagicMock()
  instance.return_value.__enter__.side_effect = (
      mocked_file_content_schema,
      mocked_file_content_file,
  )
  return instance


@pytest.fixture
def create_controller_instance(
    patch_schema: Callable[[str], None],
    patch_textfile: Callable[[str], None],
) -> Callable[[str, str], Controller]:

  def setup(schema_content: str, textfile_content: str) -> Controller:
    patch_schema(schema_content)
    patch_textfile(textfile_content)
    controller = Controller("mock/file/1", "mock/file/2")
    return controller

  return setup


@pytest.fixture
def create_mocked_controller(
    mocked_controller: mock.MagicMock,
    patch_schema: Callable[[str], None],
    patch_textfile: Callable[[str], None],
) -> Callable[[str, str], mock.Mock]:

  def setup(schema_content: str, textfile_content: str) -> mock.Mock:
    patch_schema(schema_content)
    schema = Schema("mock/schema/file/path")
    patch_textfile(textfile_content)
    mocked_controller.rules = RuleSequencer(schema)
    mocked_controller.textfile = TextFileSequencer("mock/text/file/path")
    return mocked_controller

  return setup


@pytest.fixture
def patch_schema(
    mocked_file_content_schema: StringIO,
    mocked_file_handle: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[str], None]:

  def setup(content: str) -> None:
    monkeypatch.setattr(
        "builtins.open",
        mocked_file_handle,
    )
    mocked_file_content_schema.write(content)
    mocked_file_content_schema.seek(0)

  return setup


@pytest.fixture
def patch_textfile(
    mocked_file_content_file: StringIO,
    mocked_file_handle: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> Callable[[str], None]:

  def setup(content: str) -> None:
    monkeypatch.setattr(
        "builtins.open",
        mocked_file_handle,
    )
    mocked_file_content_file.write(content)
    mocked_file_content_file.seek(0)

  return setup


@pytest.fixture
def yaml_infinite_sequence() -> str:
  return YAML_PREFIX + """
    - name: read infinite blank lines
      operation: assert_sequence_begins
      count: -1
      rules:
        - name: read blank line
          operation: assert_blank
        - name: read a
          operation: assert_equal
          expected: "a\\n"
    """ + YAML_SUFFIX


@pytest.fixture
def yaml_simple_sequence() -> str:
  return YAML_PREFIX + """
    - name: read 10 blank lines
      operation: assert_sequence_begins
      count: 10
      rules:
        - name: read blank line
          operation: assert_blank
        - name: read a
          operation: assert_equal
          expected: "a\\n"
    """ + YAML_SUFFIX


@pytest.fixture
def yaml_nested_sequence() -> str:
  return YAML_PREFIX + """
    - name: read 10 blank lines
      operation: assert_sequence_begins
      count: 10
      rules:
        - name: read 1 blank lines
          operation: assert_sequence_begins
          count: 1
          rules:
            - name: read blank line
              operation: assert_blank
            - name: read a
              operation: assert_equal
              expected: "a\\n"
    """ + YAML_SUFFIX


@pytest.fixture
def yaml_nested_infinite_sequence() -> str:
  return YAML_PREFIX + """
    - name: read infinite blank lines
      operation: assert_sequence_begins
      count: -1
      rules:
        - name: read 1 blank lines
          operation: assert_sequence_begins
          count: 1
          rules:
            - name: read blank line
              operation: assert_blank
            - name: read a
              operation: assert_equal
              expected: "a\\n"
    """ + YAML_SUFFIX
