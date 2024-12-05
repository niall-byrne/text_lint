"""Exceptions for the external operations loaders."""


class ExternalLoaderExceptionBase(OSError):
  """Base class for external loader exceptions."""


class ExternalLoaderFailedImport(ExternalLoaderExceptionBase):
  """Raised when an external loader source failed the import process."""
