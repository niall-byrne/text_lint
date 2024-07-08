"""Module entrypoint."""

from text_lint.cli.interface import TextLintCli


def cli() -> None:
  """Invoke the text_lint CLI."""

  text_lint_cli = TextLintCli()
  text_lint_cli.invoke()


if __name__ == '__main__':
  cli()
