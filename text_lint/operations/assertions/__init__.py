"""Assertion operations for text_lint."""
from typing import Dict, Type

from .assert_blank import AssertBlank
from .assert_equal import AssertEqual
from .assert_regex import AssertRegex
from .assert_regex_section import AssertRegexSection
from .assert_sequence_begins import AssertSequenceBegins
from .assert_sequence_ends import AssertSequenceEnds
from .bases.assertion_base import AssertionBase

assertion_registry: Dict[str, Type[AssertionBase]] = {
    AssertBlank.operation: AssertBlank,
    AssertEqual.operation: AssertEqual,
    AssertRegex.operation: AssertRegex,
    AssertRegexSection.operation: AssertRegexSection,
    AssertSequenceBegins.operation: AssertSequenceBegins,
    AssertSequenceEnds.operation: AssertSequenceEnds,
}
