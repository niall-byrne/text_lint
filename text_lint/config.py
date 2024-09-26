""""Temporary config file."""

import os
import re
from typing import TYPE_CHECKING

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
MAXIMUM_SUPPORTED_SCHEMA_VERSION: "AliasVersionTuple" = (0, 2, 0)
MINIMUM_SUPPORTED_SCHEMA_VERSION: "AliasVersionTuple" = (0, 0, 1)
NEW_LINE = os.linesep
SAVED_NAME_REGEX = re.compile(r'^[A-Za-z_][A-Za-z0-9_]+$')
