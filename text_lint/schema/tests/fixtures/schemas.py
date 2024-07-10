"""Schema test fixtures."""

from typing import Any, Dict

AliasRawSchema = Dict[str, Any]

one_simple_assertion: AliasRawSchema = {
    "version":
        "0.1.0",
    "settings": {
        "comment_regex": "^# ",
    },
    "assertions":
        [
            {
                "name": "basic assertion 1",
                "operation": "assert_equal",
                "expected": "#!/usr/bin/make -f\n",
                "save": "shebang",
            }
        ],
    "validators":
        [
            {
                "name": "basic assertion 1",
                "operation": "validate_debug",
                "set": ["shebang"]
            }
        ],
}

schema_missing_version: AliasRawSchema = {"ver2ion": "0.1.0"}

schema_invalid_version: AliasRawSchema = {"version": "AAA"}

schema_invalid_settings: AliasRawSchema = {
    "version": "0.1.0",
    "settings": None,
}

schema_extra_settings: AliasRawSchema = {
    "version": "0.1.0",
    "settings": {
        "comment_regex": "^#",
        "wrong_field": None,
    }
}

schema_settings_invalid_regex: AliasRawSchema = {
    "version": "0.1.0",
    "settings": {
        "comment_regex": "[s+",
    }
}

schema_missing_assertions: AliasRawSchema = {"version": "0.1.0"}

schema_empty_assertions: AliasRawSchema = {
    "version": "0.1.0",
    "assertions": [],
}

schema_missing_validators: AliasRawSchema = {
    "version":
        "0.1.0",
    "assertions":
        [
            {
                "name": "basic assertion 1",
                "operation": "assert_equal",
                "expected": "#!/usr/bin/make -f\n",
                "save": "shebang",
            }
        ],
}
