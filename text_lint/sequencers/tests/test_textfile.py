"""Test TextFileSequencer class."""

from typing import List, Type
from unittest import mock

from text_lint.schema.settings import SchemaSettings
from text_lint.sequencers.bases.sequencer_base import SequencerBase
from text_lint.sequencers.textfile import TextFileSequencer


class TestTextFileSequencer:
  """Test the TextFileSequencer class."""

  def test_initialize__attributes(
      self,
      textfile_sequencer_class: Type[TextFileSequencer],
      mocked_textfile: str,
  ) -> None:
    instance = textfile_sequencer_class(mocked_textfile)

    assert instance.path == mocked_textfile
    assert instance.index == 0

  def test_initialize__reads_specified_file(
      self,
      textfile_sequencer_class: Type[TextFileSequencer],
      mocked_open: mock.MagicMock,
      mocked_textfile: str,
  ) -> None:
    textfile_sequencer_class(mocked_textfile)

    mocked_open.assert_called_once_with(
        mocked_textfile,
        "r",
        encoding="utf-8",
    )

  def test_initialize__inheritance(
      self, textfile_sequencer_class: Type[TextFileSequencer],
      mocked_schema: mock.Mock
  ) -> None:
    instance = textfile_sequencer_class(mocked_schema)

    assert isinstance(instance, SequencerBase)

  def test_current__lines__returns_line_at_index(
      self,
      textfile_sequencer_class: Type[TextFileSequencer],
      mocked_file_content: List[str],
      mocked_textfile: str,
  ) -> None:
    instance = textfile_sequencer_class(mocked_textfile)

    received_content = []
    for line in range(0, 10):
      instance.index = line
      received_content.append(instance.current + "\n")

    assert received_content == mocked_file_content

  def test_next__iter__returns_iterator(
      self,
      textfile_sequencer_class: Type[TextFileSequencer],
      mocked_textfile: str,
  ) -> None:
    instance = textfile_sequencer_class(mocked_textfile)

    iter_instance = iter(instance)

    assert iter_instance == instance

  def test_next__lines__iterates_over_all_lines(
      self,
      textfile_sequencer_class: Type[TextFileSequencer],
      mocked_file_content: List[str],
      mocked_textfile: str,
  ) -> None:
    instance = textfile_sequencer_class(mocked_textfile)

    received_lines = [line + "\n" for line in instance]

    assert received_lines == mocked_file_content

  def test_next__lines_and_comments__iterates_over_all_lines(
      self,
      textfile_sequencer_class: Type[TextFileSequencer],
      mocked_file_content_with_comments: List[str],
      mocked_textfile: str,
  ) -> None:
    instance = textfile_sequencer_class(mocked_textfile)

    received_lines = [line + "\n" for line in instance]

    assert received_lines == mocked_file_content_with_comments

  def test_configure__comment_regex__lines_and_comments__next_skips_comments(
      self,
      textfile_sequencer_class: Type[TextFileSequencer],
      mocked_file_content_with_comments: List[str],
      mocked_textfile: str,
  ) -> None:
    mocked_comment_regex = "^#"
    mocked_schema = mock.Mock()
    mocked_schema.settings = SchemaSettings(comment_regex=mocked_comment_regex)

    instance = textfile_sequencer_class(mocked_textfile)

    instance.configure(mocked_schema)
    received_lines = [line + "\n" for line in instance]

    assert received_lines == (
        mocked_file_content_with_comments[1:3] +
        mocked_file_content_with_comments[4:]
    )

  def test_configure__no_comment_regex__lines_and_comments__next_all_lines(
      self,
      textfile_sequencer_class: Type[TextFileSequencer],
      mocked_file_content_with_comments: List[str],
      mocked_textfile: str,
  ) -> None:
    mocked_schema = mock.Mock()
    mocked_schema.settings = SchemaSettings()

    instance = textfile_sequencer_class(mocked_textfile)

    instance.configure(mocked_schema)
    received_lines = [line + "\n" for line in instance]

    assert received_lines == mocked_file_content_with_comments
