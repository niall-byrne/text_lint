# Usage examples of text_lint

This project lints it's Makefile using text_lint:
- the schema file is found [here](../schemas/makefile.yml)
- the Makefile itself is found [here](../Makefile)

Walking through these example files while reading the following description is intended to provide a starting point for writing new schema files.

### Schema Description

Initially the schema declares which schema `version` it's using.  This ensures that the installed version of text_lint is compatible with it.

Next a regex is defined that identifies lines that will be ignored (`comments`) in the target file during linting.

The file defines two subsections for parsing rules and result validators.

### Rules

The `rules` section is mandatory.  Here the schema asserts what content the target file is expected to have using text_lint `assertion operations`.

Each of these operations defines an expected target file line, or lines, that must exist in the order determined by the operations themselves.  These assertions effectively describe the target file as a whole.

The `assert_sequence_begins` assertion allows us to apply a repeating series of assertions to the target file.  This can be an infinite (`count: -1`) or bounded set of repeating rules.

A failure of any individual assertion operation to pass or the inability to read the entire text file is a failure of the linting process.

Assertion operations also provide the ability to capture results via [regular expression](https://en.wikipedia.org/wiki/Regular_expression) capture groups.  This allows additional processing on in the [validation](#validators) stage to further validate the target file.

It's important to have a good grasp of writing regular expressions to make the most of text_lint.

To see the available assertion operations, take a look at the [schema documentation](SCHEMA.md).

The text_lint CLI can also help with this:

```shell
    text_lint list
    text_lint doc assert_equal
    text_lint doc assert_regex
```

### Validators

The validators section is also mandatory, but it need not contain rules:

```yaml

validators: []
```

This schema has a number of `validation operations` that consume the `saved` result values that were created by the assertion operation rules.  These validation operations then combine and compare the values to ensure the target file is correctly structured.

The validation operations are composed of `lookup operations` that select and transform the saved result values.  This allows selecting different capture groups, sorting the values, and transforming the selected values into new ones.  They are formed by creating dot separated `lookup expressions` that start with the name of a saved result value and then chain the various lookup operations together.

Some lookup operations are meant for transforming data, and all start with the same indicator `to` (i.e. to_json, to_sorted, to_unique).  These `transformation lookups` are meant to be placed at the end of the lookup expression to produce a final value.

Other lookup operations are prefixed with `~` to indicate they are static values, and are meant to be interpreted as just the text itself (i.e. `~help` for the word 'help').

Finally, you can also extract specific characters from words or entries in lists by adding digits to your lookup expressions (i.e. `result.capture.0`).

The `validate_debug` operation is incredibly useful when writing lookup expressions, giving a look at the underlying data being manipulated.

To see the available validation and lookup operations, take a look at the [schema documentation](SCHEMA.md).

The text_lint CLI can also help with this:

```shell
    text_lint list
    text_lint doc validate_debug
    text_lint doc capture
    text_lint doc to_upper
```
