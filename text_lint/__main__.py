"""Module entrypoint."""

import argparse
import os

from .controller import Controller
from .controller.settings import ControllerSettings


def file_type(filename: str) -> str:
  if os.path.exists(filename):
    return os.path.abspath(filename)
  raise FileNotFoundError(filename)


def cli() -> None:
  """Parse the command line arguments."""

  parser = argparse.ArgumentParser(
      prog="text_lint",
      description="Generic text file linter.",
  )
  required = parser.add_argument_group("required arguments")
  required.add_argument(
      "filename",
      help="the text file to lint",
      type=file_type,
      nargs="+",
  )
  required.add_argument(
      "-s",
      "--schema",
      help="the schema to apply",
      required=True,
      type=str,
  )
  args = parser.parse_args()

  for filename in args.filename:
    settings = ControllerSettings(
        file_path=filename,
        schema_path=args.schema,
    )
    ctrl = Controller(settings=settings)
    ctrl.start()


if __name__ == "__main__":
  cli()
