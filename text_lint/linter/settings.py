"""LinterSettings class."""


class LinterSettings:
  """Linter settings."""

  def __init__(
      self,
      file_path: str,
      interpolate_schema: bool,
      quiet: bool,
      schema_path: str,
  ) -> None:
    """Initialize LinterSettings instances.

    :param file_path:  The absolute path to the file being linted.
    :param interpolate_schema:  Controls schema variable interpolation.
    :param quiet:  Controls linter verbosity.
    :param schema_path:  The absolute path to the schema file.
    """
    self.file_path = file_path
    self.interpolate_schema = interpolate_schema
    self.quiet = quiet
    self.schema_path = schema_path
