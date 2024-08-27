# Installing text_lint

This tool requires Python version 3.6 or later to be installed.

## Python Library

Installation of text_lint is fairly straightforward from [PyPi](https://pypi.org/project/text-lint/):

```shell
    pip install text_lint
```

You'll then be able to interact with the tool directly:

```shell
    text_lint
    python -m text_lint
```

## With Pre-Commit

Adding text_lint to your [pre-commit](https://pre-commit.com/index.html) tool chain is also fairly straightforward.
Add a stanza to your `.pre-commit-config.yaml` file identifying the schema file to use and the types of files to use it on:

```yaml
  - repo: https://github.com/niall-byrne/text_lint
    rev: v0.0.1
    hooks:
      - id: text_lint
        name: "Enforce a text file schema"
        args:
          - "-s"
          - "path/to/my/schema"
        files: "^.+\\.txt$"
        stages: [pre-commit]
```
