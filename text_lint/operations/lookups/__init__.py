"""Parser result lookups for text_lint."""

from collections import defaultdict
from typing import Dict, Type

from text_lint.config import LOOKUP_SENTINEL
from .bases.lookup_base import LookupBase
from .capture import CaptureLookup
from .default import DefaultLookup
from .group import GroupLookup
from .index import IndexLookup
from .name import NameLookup
from .noop import NoopLookup
from .to_count import CountLookup
from .to_json import JsonLookup
from .to_lower import LowerLookup
from .to_reversed import ReversedLookup
from .to_sorted import SortedLookup
from .to_unique import UniqueLookup
from .to_upper import UpperLookup
from .unique import UniqueFilterLookup

lookup_registry: Dict[str, Type[LookupBase]] = defaultdict(
    lambda: DefaultLookup, {
        LOOKUP_SENTINEL: NoopLookup,
        CaptureLookup.operation: CaptureLookup,
        CountLookup.operation: CountLookup,
        GroupLookup.operation: GroupLookup,
        JsonLookup.operation: JsonLookup,
        LowerLookup.operation: LowerLookup,
        NoopLookup.operation: NoopLookup,
        ReversedLookup.operation: ReversedLookup,
        SortedLookup.operation: SortedLookup,
        UniqueFilterLookup.operation: UniqueFilterLookup,
        UniqueLookup.operation: UniqueLookup,
        UpperLookup.operation: UpperLookup,
    }
)
