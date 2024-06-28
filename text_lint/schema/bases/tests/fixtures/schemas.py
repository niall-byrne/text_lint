"""SchemaSectionBase test fixtures."""

from typing import Any, Dict, List

AliasRawSchemaRules = List[Dict[str, Any]]

one_simple_rule: AliasRawSchemaRules = [
    {
        "name": "basic rule 1",
        "operation": "A"
    }
]

two_simple_rules: AliasRawSchemaRules = [
    {
        "name": "basic rule 1",
        "operation": "A"
    },
    {
        "name": "basic rule 2",
        "operation": "B"
    },
]

invalid_operation: AliasRawSchemaRules = [
    {
        "name": "basic rule 1",
        "operation": "INVALID"
    }
]
