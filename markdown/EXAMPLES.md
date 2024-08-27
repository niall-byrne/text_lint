# Usage examples of text_lint

This project lints its own Makefile using `text_lint`:
- the schema file can be found [here](../schemas/makefile.yml)
- the Makefile itself can be found [here](../Makefile)

Viewing these example files side-to-side with the guide below provides the context needed to start building new schemas.

## Schema Introduction

The schema file is a declaration of what your target file(s) SHOULD look like.  

This [YAML](https://yaml.org/) document describes the structure and contents of your target file(s) without being overly verbose.

### Version and Settings

Initially the schema declares which `version` it's using.  This ensures that the installed version of `text_lint` is compatible.

Next a regex is defined that identifies lines that will be ignored (`comments`) in the target file during checks.  This could be also set to `null` to disable this feature.

### Assertions

The `assertions` section is mandatory.  Here the schema asserts what content the target file is expected to have using `assertion operations`.

Each of these operations declares what **sequential** target file line (or lines) should consist of.  Together these assertions describe the structure of the file(s) as a whole.

#### Sequences

The `assert_sequence_begins` assertion allows us to apply a repeating series of assertions to the target file.  This can be an infinite (`count: -1`) or bounded set of repeating assertions.

#### Check Failures

A failure of any individual assertion operation to pass or the inability to process the entire text file is considered a failure of the check process.

#### Save IDs

Assertion operations also provide the ability to save extracted values via [regular expression](https://en.wikipedia.org/wiki/Regular_expression) capture groups.  This allows additional processing in the [validation](#validators) stage.

Each of these extracted values is given a `save id` which is used by the `validation operations` to perform additional processing.

#### Regular Expressions

It's important to have a good grasp of writing regular expressions to make the most of `text_lint`.  Also make sure to follow the rule of `double escaping`:

```yaml
  - regex: "^\s+([a-z])+$"    # This won't be parsed correctly
  - regex: "^\\s+([a-z])+$"   # Do this instead.
```

#### Assertion Documentation

To see a list of available assertion operations or for details on each one, please use the `text_lint` CLI:

```shell
    text_lint list
    text_lint doc assert_equal
    text_lint doc assert_regex
```

### Validators

The `validators` section is also mandatory, but it can be defined as an empty list if extra validation is not required.

The `validation operations` consumes `save id` values that were created by the assertion operations.  These validation operations then combine and compare the values to ensure the content of the target file(s) is correct.

#### Lookup Expressions

The validation operations themselves are built by combining `lookup operations` into `lookup expressions`.  This is how the `save id` values are manipulated.

To write a `lookup expression`, start with a `save id` and then chain dot-separated `lookup operations`:
  - `save_id_1.lookup_operation()`
  - `save_id_2.lookup_operation().lookup_operation()`

This allows selecting different capture groups, sorting the values, and transforming the selected values into new ones.

Here are a few concrete examples of actual lookup expressions:
  - `save_id_1.to_lower()`
  - `save_id_2.capture(1).unique()`
  - `save_id_3.capture(1).1.to_upper()`

#### Positional Lookup Operations

There are a couple of lookup operations that are restricted in their usage.  They are not intended to be called multiple times within a lookup expression, and *must* be placed *before* any [transformation lookup operations](#transformation-lookup-operations).

Specifically these positional lookups are:
  - `capture`: which extracts a specific capture group from a save id.  It should only be used once per lookup expression, as it makes little sense to perform operations on a capture group and then switch to a different capture group.
  - `as_json`: which shows a json representation of a save id.  This too should only be used once per lookup expression, as it generates a completely new result value.  (Use `as_json` with `validate_debug` when working with complex loops to assist in writing lookup expressions.)

#### Transformation Lookup Operations

Some lookup operations are meant for transforming data, and all start with the same indicator '`to`' (i.e. `to_sorted`, `to_unique`).

These `transformation lookups` are meant to be placed at the end of the lookup expression to produce a final value.

#### Static Values

Other lookup operations are prefixed with `~` to indicate they are static values, and are meant to be interpreted as just the text itself (i.e. `~help` for the word 'help').

#### Index Lookups

Finally, you can also extract specific characters from words or entries in arrays by adding digits to your lookup expressions:
  - `save_id_1.to_lower().0`
  - `save_id_2.capture(1).unique().3`

#### Lookups

The `validate_debug` operation is incredibly useful when writing lookup expressions, giving a look at the underlying data being manipulated.

An example `validate_debug` operation might look like:

```yaml
  - name: debug extracted sub_headers
    operation: validate_debug
    saved:
      - sub_headings.capture(1)
      - sub_headings.as_json()
```

#### Lookup and Validator Documentation

To see a list of available validation and lookup operations or for details on each one, please use the `text_lint` CLI:

```shell
    text_lint list
    text_lint doc validate_debug
    text_lint doc capture
    text_lint doc to_upper
```

## Summary

Schemas must contain the following information:
- version identifier
- comment regular expression
- an assertion section
- a validator section

The [assertion section](#assertions) must contain one or more `assertion operations` that describe the structure of each text file.

The [validators section](#validators) *may* contain `validation operations` to examine the content of each text file with more scrutiny.  Combine `lookup operations` into [lookup expressions](#lookup-expressions) to create complex validation logic.

The `text_lint` CLI is the best source for authoritative documentation on how to use each assertion, validator and lookup operation.
