# text_lint

[![cicd-tools](https://img.shields.io/badge/ci/cd:-cicd_tools-blue)](https://github.com/cicd-tools-org/cicd-tools)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

| Branch                                                     | Build                                                                                                                                                                                                |
|------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [main](https://github.com/niall-byrne/text_lint/tree/main) | [![workflow-link](https://github.com/niall-byrne/text_lint/actions/workflows/workflow-push.yml/badge.svg?branch=main)](https://github.com/niall-byrne/text_lint/actions/workflows/workflow-push.yml) |
| [dev](https://github.com/niall-byrne/text_lint/tree/dev)   | [![workflow-link](https://github.com/niall-byrne/text_lint/actions/workflows/workflow-push.yml/badge.svg?branch=dev)](https://github.com/niall-byrne/text_lint/actions/workflows/workflow-push.yml)  |

Define a custom YAML schema and use it to validate text files.

## Use Cases

Create custom linters for plain text files in CI/CD pipelines:
  - Makefiles
  - YAML configuration files

Audit groups of text files to enforce a common schema:
  - Check header fields in Markdown files (i.e. for knowledge bases such as Obsidian)
  - Check for duplicate entries or duplicate headers

## Documentation

- Learn to use `text_lint` through a [real usage example](https://text-lint.readthedocs.io/latest/usage/examples.html).
- See some [common recipes](https://text-lint.readthedocs.io/latest/usage/recipes.html) for useful lookup expressions.

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

There is help documentation in the CLI that is the best reference for how to use the various `Assertions`, `Lookups` and `Validations` that make up the `text_lint` ecosystem.

Before diving into all that though, it might be helpful to look at a usage [example](https://text-lint.readthedocs.io/latest/usage/examples.html).

## Pre-Commit Integration

Adding `text_lint` to your [pre-commit](https://pre-commit.com/index.html) tool chain is also fairly straightforward.

An example can be found in the [documentation](https://text-lint.readthedocs.io/latest/usage/getting_started.html#pre_commit_integration).
