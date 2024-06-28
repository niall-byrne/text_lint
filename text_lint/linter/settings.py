"""Linter settings class."""


class LinterSettings:
  """Linter settings."""

  def __init__(
      self,
      file_path: str,
      schema_path: str,
  ) -> None:
    self.file_path = file_path
    self.schema_path = schema_path
