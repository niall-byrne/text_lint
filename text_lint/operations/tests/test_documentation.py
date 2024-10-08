"""Tests for the OperationDocumentation class."""

import random
from typing import TYPE_CHECKING, List, Tuple, Type
from unittest import mock

import pytest
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOKUP_STATIC_VALUE_MARKER, NEW_LINE
from text_lint.operations.lookups import (
    IndexLookup,
    LowerLookup,
    NameLookup,
    lookup_registry,
)
from text_lint.operations.rules import AssertBlank, rule_registry
from text_lint.operations.validators import ValidateDebug, validator_registry
from ..documentation import REGISTRY_NAMES, OperationDocumentation

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.operations.bases.operation_base import OperationBase
  from ..documentation import AliasRegistry


class TestOperationDocumentation:
  """Tests for the OperationDocumentation class."""

  def filter(
      self,
      registry: "AliasRegistry",
  ) -> "AliasRegistry":
    return {
        operation_name: operation_class
        for (operation_name, operation_class) in registry.items()
        if not operation_class.internal_use_only
    }

  def test_initialize__attributes(self) -> None:
    instance = OperationDocumentation()

    assert instance.content == ""
    assert instance.registries[REGISTRY_NAMES[0]] == self.filter(rule_registry)
    assert instance.registries[REGISTRY_NAMES[1]
                              ] == self.filter(validator_registry)
    assert instance.registries[REGISTRY_NAMES[2]
                              ] == self.filter(lookup_registry)

  def test_initialize__translations(self) -> None:
    instance = OperationDocumentation()

    assert len(instance.msg_fmt_operation_list_headers) == 2
    for header in instance.msg_fmt_operation_list_headers:
      assert_is_translated(header)
    assert len(instance.msg_fmt_operation_doc_headers) == 4
    for header in instance.msg_fmt_operation_doc_headers:
      assert_is_translated(header)
    assert_is_translated(instance.msg_fmt_operation_unknown)

  def test_list__creates_correct_title(self) -> None:
    instance = OperationDocumentation()

    instance.list()

    assert NEW_LINE.join(instance.content.split(NEW_LINE)[0:3]) == "".join(
        [
            instance.msg_fmt_operation_list_headers[0],
            NEW_LINE,
            "-" * len(instance.msg_fmt_operation_list_headers[0]),
            NEW_LINE,
        ]
    )

  @pytest.mark.parametrize("registry", REGISTRY_NAMES)
  def test_list__vary_registry__generates_correct_content(
      self,
      registry: str,
  ) -> None:
    instance = OperationDocumentation()

    instance.list()

    indexed_content = instance.content.split(NEW_LINE)
    index = indexed_content.index(
        instance.msg_fmt_operation_list_headers[1].format(registry)
    )
    for operation in sorted(instance.registries[registry]):
      index += 1
      assert indexed_content[index] == "".join(
          [
              "  ",
              operation.ljust(24),
              instance.registries[registry][operation].hint,
          ]
      )

  @pytest.mark.parametrize(
      "operation_class,operation_name,registry_type",
      [
          (AssertBlank, AssertBlank.operation, REGISTRY_NAMES[0]),
          (ValidateDebug, ValidateDebug.operation, REGISTRY_NAMES[1]),
          (LowerLookup, LowerLookup.operation, REGISTRY_NAMES[2]),
          (
              NameLookup, LOOKUP_STATIC_VALUE_MARKER + "named_value",
              REGISTRY_NAMES[2]
          ),
          (
              IndexLookup,
              str(round(random.SystemRandom().random() * 100)),
              REGISTRY_NAMES[2],
          ),
      ],
  )
  def test_search__vary_valid_operation__generates_correct_content(
      self,
      operation_class: Type["OperationBase"],
      operation_name: str,
      registry_type: str,
  ) -> None:
    instance = OperationDocumentation()
    fmt_contents: List[Tuple[str, str]] = [
        (operation_class.operation, NEW_LINE),
        (registry_type, NEW_LINE),
        (operation_class.hint, NEW_LINE),
        (operation_class.yaml_example, ""),
    ]
    expected_content = "".join(
        [
            msg_fmt.format(fmt_content[0]) + fmt_content[1]
            for msg_fmt, fmt_content in
            zip(instance.msg_fmt_operation_doc_headers, fmt_contents)
        ]
    )

    instance.search(operation_name)

    assert instance.content == expected_content

  def test_search__invalid_operation__generates_correct_content(self,) -> None:
    instance = OperationDocumentation()
    invalid_operation = "invalid_operation"
    expected_translations = mock.call(
        instance.msg_fmt_operation_unknown,
        invalid_operation,
    )
    expected_content = expected_translations.args[0].format(
        expected_translations.args[1]
    )

    instance.search(invalid_operation)

    assert instance.content == expected_content

  @pytest.mark.parametrize("mocked_message", ["message1", "message2"])
  def test_print__vary_message__writes_to_stdout(
      self,
      capfd: pytest.CaptureFixture[str],
      mocked_message: str,
  ) -> None:
    instance = OperationDocumentation()
    instance.content = mocked_message

    instance.print()

    stdout, stderr = capfd.readouterr()
    assert stdout == mocked_message + NEW_LINE
    assert stderr == ""
