"""Parser rules for text_lint."""
from typing import Dict, Type

from .assert_blank import AssertBlank
from .assert_equal import AssertEqual
from .assert_regex import AssertRegex
from .assert_regex_section import AssertRegexSection
from .assert_sequence_begins import AssertSequenceBegins
from .assert_sequence_ends import AssertSequenceEnds
from .bases.rule_base import RuleBase

rule_registry: Dict[str, Type[RuleBase]] = {
    AssertBlank.operation: AssertBlank,
    AssertEqual.operation: AssertEqual,
    AssertRegex.operation: AssertRegex,
    AssertRegexSection.operation: AssertRegexSection,
    AssertSequenceBegins.operation: AssertSequenceBegins,
    AssertSequenceEnds.operation: AssertSequenceEnds,
}
