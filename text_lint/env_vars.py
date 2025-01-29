"""Core environment variable definitions."""

from text_lint.utilities.documentation import document_module_attributes

EXTENSIONS_LOCAL_ENV_VAR = "TEXT_LINT_EXTENSIONS_LOCAL_FOLDER"
EXTENSIONS_LOCAL_VAR_SEPERATOR = ":"
EXTENSIONS_THIRD_PARTY_ENV_VAR = "TEXT_LINT_EXTENSIONS_THIRD_PARTY"
EXTENSIONS_THIRD_PARTY_VAR_SEPERATOR = ":"

document_module_attributes(
    __name__,
    [
        "The environment variable name for local extensions folders.",
        "The seperator string to extract individual local extensions folders.",
        "The environment variable name for third party extensions modules.",
        "The seperator string to extract third party extensions modules.",
    ],
)
