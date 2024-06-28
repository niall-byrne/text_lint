"""SchemaSectionBase test fixtures."""

from typing import Any, Dict, List

AliasRawSchemaAssertions = List[Dict[str, Any]]

one_simple_assertion: AliasRawSchemaAssertions = [
    {
        "name": "basic assertion 1",
        "operation": "A"
    }
]

two_simple_assertions: AliasRawSchemaAssertions = [
    {
        "name": "basic assertion 1",
        "operation": "A"
    },
    {
        "name": "basic assertion 2",
        "operation": "B"
    },
]

invalid_operation: AliasRawSchemaAssertions = [
    {
        "name": "basic assertion 1",
        "operation": "INVALID"
    }
]
