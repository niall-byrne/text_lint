"""Lookup operations for text_lint."""

from collections import defaultdict
from typing import Dict, Type

from text_lint.config import LOOKUP_SENTINEL
from .as_json import JsonLookup
from .bases.lookup_base import LookupBase
from .capture import CaptureLookup
from .default import DefaultLookup
from .name import NameLookup
from .noop import NoopLookup
from .to_group import GroupLookup
from .to_lower import LowerLookup
from .to_unique import UniqueLookup
from .to_upper import UpperLookup

lookup_registry: Dict[str, Type[LookupBase]] = defaultdict(
    lambda: DefaultLookup, {
        LOOKUP_SENTINEL: NoopLookup,
        CaptureLookup.operation: CaptureLookup,
        GroupLookup.operation: GroupLookup,
        JsonLookup.operation: JsonLookup,
        LowerLookup.operation: LowerLookup,
        NoopLookup.operation: NoopLookup,
        UniqueLookup.operation: UniqueLookup,
        UpperLookup.operation: UpperLookup,
    }
)
