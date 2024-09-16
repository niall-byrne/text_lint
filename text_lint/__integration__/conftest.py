"""Shared integration test fixtures."""
# pylint: disable=redefined-outer-name

from io import StringIO
from typing import Callable
from unittest import mock

import pytest
from text_lint.linter import Linter
from text_lint.linter.settings import LinterSettings
from text_lint.linter.states import StateFactory
from text_lint.schema import Schema
from text_lint.sequencers.assertions import AssertionSequencer
from text_lint.sequencers.textfile import TextFileSequencer

YAML_PREFIX = """
---
version: "0.1.0"

settings:
  comment_regex: "^(#\\\\s|#[^!]).+$"

assertions:
"""

YAML_SUFFIX = """
validators: []
"""


@pytest.fixture
def mocked_linter() -> mock.MagicMock:
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
def create_linter_instance(
    patch_schema: Callable[[str], None],
    patch_textfile: Callable[[str], None],
) -> Callable[[str, str], Linter]:

  def setup(schema_content: str, textfile_content: str) -> Linter:
    patch_schema(schema_content)
    patch_textfile(textfile_content)
    settings = LinterSettings(
        file_path="mock/file/1",
        interpolate_schema=False,
        schema_path="mock/file/2",
    )
    linter = Linter(settings=settings)
    return linter

  return setup


@pytest.fixture
def create_mocked_linter(
    mocked_linter: mock.MagicMock,
    patch_schema: Callable[[str], None],
    patch_textfile: Callable[[str], None],
) -> Callable[[str, str], mock.Mock]:

  def setup(schema_content: str, textfile_content: str) -> mock.Mock:
    patch_schema(schema_content)
    schema = Schema("mock/schema/file/path", False)
    patch_textfile(textfile_content)
    mocked_linter.assertions = AssertionSequencer(schema)
    mocked_linter.state = StateFactory(mocked_linter)
    mocked_linter.textfile = TextFileSequencer("mock/text/file/path")
    return mocked_linter

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
      assertions:
        - name: read blank line
          operation: assert_blank
        - name: read a
          operation: assert_equal
          expected: "a"
    """ + YAML_SUFFIX


@pytest.fixture
def yaml_simple_sequence() -> str:
  return YAML_PREFIX + """
    - name: read 10 blank lines
      operation: assert_sequence_begins
      count: 10
      assertions:
        - name: read blank line
          operation: assert_blank
        - name: read a
          operation: assert_equal
          expected: "a"
    """ + YAML_SUFFIX


@pytest.fixture
def yaml_nested_sequence() -> str:
  return YAML_PREFIX + """
    - name: read 10 blank lines
      operation: assert_sequence_begins
      count: 10
      assertions:
        - name: read 1 blank lines
          operation: assert_sequence_begins
          count: 1
          assertions:
            - name: read blank line
              operation: assert_blank
            - name: read a
              operation: assert_equal
              expected: "a"
    """ + YAML_SUFFIX


@pytest.fixture
def yaml_nested_infinite_sequence() -> str:
  return YAML_PREFIX + """
    - name: read infinite blank lines
      operation: assert_sequence_begins
      count: -1
      assertions:
        - name: read 1 blank lines
          operation: assert_sequence_begins
          count: 1
          assertions:
            - name: read blank line
              operation: assert_blank
            - name: read a
              operation: assert_equal
              expected: "a"
    """ + YAML_SUFFIX
