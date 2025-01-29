"""Core application configuration."""

import os
import re
from typing import TYPE_CHECKING

from text_lint.utilities.documentation import document_module_attributes

if TYPE_CHECKING:  # pragma: no cover
  from .version import AliasVersionTuple

LOGGING_COLUMN1_WIDTH = 15
LOGGING_COLUMN2_WIDTH = 30
LOGGING_INDENT = "  "
LOOKUP_SENTINEL = ""
LOOKUP_SEPERATOR = "."
LOOKUP_STATIC_VALUE_MARKER = "~"
LOOKUP_TRANSFORMATION_PREFIX = "to_"
LOOKUP_NAME_REGEX = re.compile(r'^([A-Za-z_]+)\((.*)\)$')
LOOP_COUNT = -1
LOOP_RECURSION_LIMIT = 100
MAXIMUM_SUPPORTED_SCHEMA_VERSION: "AliasVersionTuple" = (0, 2, 0)
MINIMUM_SUPPORTED_SCHEMA_VERSION: "AliasVersionTuple" = (0, 0, 1)
NEW_LINE = os.linesep
SAVED_NAME_REGEX = re.compile(r'^[A-Za-z_][A-Za-z0-9_]+$')

document_module_attributes(
    __name__,
    [
        "The number of characters in logging column 1.",
        "The number of characters in logging column 2.",
        "The logging indentation string.",
        "The sentinel value used by default to identify lookups.",
        "The string used to separate each lookup in a lookup expression.",
        "The string used to identify static values in a lookup expression.",
        "The string used to identify transformation lookup operations.",
        "A regular expression to validate lookup operation names.",
        "A loop count value that indicates an infinite loop.",
        "The linter's recursion limit for deeply nested sequences.",
        "The minimum schema version this application with support.",
        "The maximum schema version this application with support.",
        "The new line seperator value used by the application.",
        "A regular expression to validate save id names.",
    ],
)
