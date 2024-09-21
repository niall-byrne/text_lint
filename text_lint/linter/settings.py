"""Linter settings class."""


class LinterSettings:
  """Linter settings."""

  def __init__(
      self,
      file_path: str,
      interpolate_schema: bool,
      quiet: bool,
      schema_path: str,
  ) -> None:
    self.file_path = file_path
    self.interpolate_schema = interpolate_schema
    self.quiet = quiet
    self.schema_path = schema_path
