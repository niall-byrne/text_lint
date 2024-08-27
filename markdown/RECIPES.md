# The `text_lint` Lookup Expression Cookbook

These examples are designed to give you an idea of how to make the most of the existing built-in lookups.

## Alphabetical Order

```yaml
validators:

    # Lookup Expression Recipe:
    # 1. Split the value by space
    # 2. Sort one side of the comparison lookup
    # 3. Compare the values

  - name: create test value
    operation: validate_combine
    saved:
      - ~Zebra Apple Banana Cantaloupe Date
    new_saved: test_value

  - name: enforce alphabetical order
    operation: validate_equal
    saved_a:
      - test_value.capture(1).to_split(" ")
    saved_b:
      - test_value.capture(1).to_split(" ").to_sorted()

```

## Counting Words

```yaml
validators:

    # Lookup Expression Recipe:
    # 1. Split the value by space
    # 2. Optionally convert the case
    # 3. Split the single list up into multiple to allow counting occurrences
    # 4. Search for a static value
    # 5. Group the outer results together to allow counting the inner occurrences

  - name: create test value
    operation: validate_combine
    saved:
      - ~Sequence of Repeating Repeating repeating words.
    new_saved: test_value

  - name: word count example lookups
    operation: validate_debug
    saved:
      # Case Sensitive
      - test_value.capture(1).to_split(" ").to_split().~repeating.to_group().to_count()
      # Case Insensitive
      - test_value.capture(1).to_lower().to_split(" ").to_split().~repeating.to_group().to_count()
```

## Duplicate Values

```yaml
validators:

    # Lookup Expression Recipe:
    # 1. Split the value by space
    # 2. Optionally convert the case
    # 3. Make one side of the comparison unique values
    # 4. Compare the values

  - name: create test value
    operation: validate_combine
    saved:
      - ~Sequence of Repeating Repeating repeating words.
    new_saved: test_value

  - name: duplicate word detection (case sensitive)
    operation: validate_equal
    saved_a:
      - test_value.capture(1).to_split(" ").to_unique()
    saved_b:
      - test_value.capture(1).to_split(" ")
  
  - name: duplicate word detection (case insensitive)
    operation: validate_equal
    saved_a:
      - test_value.capture(1).to_lower().to_split(" ").to_unique()
    saved_b:
      - test_value.capture(1).to_lower().to_split(" ")
```
