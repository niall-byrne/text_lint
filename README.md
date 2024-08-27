# text_lint

Define a custom YAML schema and use it to validate text files.

## Use Cases

Create custom linters for plain text files in CI/CD pipelines:
  - Makefiles
  - YAML configuration files

Audit groups of text files to enforce a common schema:
  - Check header fields in Markdown files (i.e. for knowledge bases such as Obsidian)
  - Check for duplicate entries or duplicate headers

## Documentation

- Learn to use `text_lint` through a [real usage example](markdown/EXAMPLES.md).
- See some [common recipes](markdown/RECIPES.md) for useful lookup expressions.

## CLI Installation

This tool requires Python version 3.6 or later.

Use [pip](https://pypi.org/project/pip/) to install `text_lint` from [PyPi](https://pypi.org/project/text-lint/).

### Python Versions Below 3.8

Older versions of Python require a workaround for [PyYAML](https://pypi.org/project/PyYAML/), but it's fairly straightforward:

```shell
  echo "cython<3" > /tmp/constraint.txt
  export PIP_CONSTRAINT=/tmp/constraint.txt
  pip install text_lint
```

### Python Versions 3.8 and Above

```shell
    pip install text_lint
```

### Launching `text_lint`

```shell
    text_lint
    python -m text_lint
```

There is comprehensive documentation in the CLI that is the best reference for how to use the various `Assertions`, `Lookups` and `Validations` that make up the `text_lint` ecosystem.

## Pre-Commit Integration

Adding `text_lint` to your [pre-commit](https://pre-commit.com/index.html) tool chain is also fairly straightforward.

Add a stanza to your `.pre-commit-config.yaml` file identifying the schema file to use and the types of files to use it on:

```yaml
  - repo: https://github.com/niall-byrne/text_lint
    rev: v0.1.0
    hooks:
      - id: text_lint
        name: "Enforce a text file schema"
        args:
          - "check"
          - "-s"
          - "path/to/my/schema"
        files: "^.+\\.txt$"
        stages: [pre-commit]
```
