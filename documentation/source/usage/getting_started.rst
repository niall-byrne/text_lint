Getting Started
===============

CLI Installation
----------------

This tool requires Python version 3.6 or later.

Python Versions Below 3.8
~~~~~~~~~~~~~~~~~~~~~~~~~

Older versions of Python require a workaround for `PyYAML <https://pypi.org/project/PyYAML/>`__, but it's fairly straightforward:

.. code:: yaml

     echo "cython<3" > /tmp/constraint.txt
     export PIP_CONSTRAINT=/tmp/constraint.txt
     pip install text_lint

Python Versions 3.8 and Above
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This isn't required on more modern Python versions:

.. code:: yaml

     pip install text_lint


Launching
~~~~~~~~~

The CLI can be invoked by either calling the ``text_lint`` shim or the module itself:

.. code:: yaml

     text_lint
     python -m text_lint


There is help documentation in the CLI that is the best reference for how to use the various ``Assertions``, ``Lookups`` and ``Validations`` that make up the ``text_lint`` ecosystem.


.. _pre_commit_integration:

Pre-Commit Integration
----------------------

When using ``text_lint`` on files within a git codebase, integrating it with `pre-commit <https://pre-commit.com/index.html>`__ is often desirable.

Add a stanza to the `.pre-commit-config.yaml` file identifying the schema file to use and the types of files to use it on:


.. code:: yaml

     - repo: https://github.com/niall-byrne/text_lint
       rev: v0.1.0
       hooks:
         - id: text_lint
           name: "Enforce a text file schema"
           args:
             - "check"
             - "-s"
             - "path/to/my/schema.yml"
           files: "^.+\\.txt$"
           stages: [pre-commit]
