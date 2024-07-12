"""Test the DefaultLookup class."""

from typing import Dict
from unittest import mock

import pytest
from text_lint.__helpers__.lookups import (
    assert_is_lookup_unknown,
    generate_result_index,
    generate_static_name,
    generated_valid_default_lookup_test_cases,
)
from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.config import LOOKUP_STATIC_VALUE_MARKER
from text_lint.exceptions.lookups import LookupUnknown
from ..bases.lookup_base import LookupBase
from ..default import YAML_EXAMPLE, DefaultLookup


class TestDefaultLookup:
  """Test the DefaultLookup class."""

  @generated_valid_default_lookup_test_cases
  def test_initialize__vary_lookup_name__attributes(
      self,
      mocked_lookup_expression: mock.Mock,
      lookup_name: str,
      mocked_requesting_operation_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint":
            (
                "handler for unknown lookups which may be "
                "static values or indexes"
            ),
        "internal_use_only": True,
        "is_positional": False,
        "lookup_expression": mocked_lookup_expression,
        "lookup_name": lookup_name,
        "operation": "default",
        "requesting_operation_name": mocked_requesting_operation_name,
        "yaml_example": YAML_EXAMPLE,
    }

    instance = DefaultLookup(
        lookup_name,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )

    assert_operation_attributes(instance, attributes)

  @generated_valid_default_lookup_test_cases
  def test_initialize__vary_lookup_name__translations(
      self,
      mocked_lookup_expression: mock.Mock,
      lookup_name: str,
      mocked_requesting_operation_name: str,
  ) -> None:
    instance = DefaultLookup(
        lookup_name,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )

    assert_is_translated(instance.hint)

  @generated_valid_default_lookup_test_cases
  def test_initialize__vary_lookup_name__inheritance(
      self,
      mocked_lookup_expression: mock.Mock,
      lookup_name: str,
      mocked_requesting_operation_name: str,
  ) -> None:
    instance = DefaultLookup(
        lookup_name,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )

    assert_operation_inheritance(
        instance,
        bases=(LookupBase, DefaultLookup),
    )

  def test_apply__result_index__applies_index_lookup(
      self,
      mocked_default_subclasses: Dict[str, mock.Mock],
      mocked_lookup_expression: mock.Mock,
      mocked_requesting_operation_name: str,
      mocked_state: mock.Mock,
  ) -> None:
    index = generate_result_index()

    instance = DefaultLookup(
        index,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )

    instance.apply(mocked_state)

    mocked_default_subclasses["IndexLookup"].assert_called_once_with(
        index,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )
    mocked_default_subclasses["IndexLookup"].\
        return_value.apply.assert_called_once_with(mocked_state)

  def test_apply__result_index__does_not_apply_name_lookup(
      self,
      mocked_default_subclasses: Dict[str, mock.Mock],
      mocked_lookup_expression: mock.Mock,
      mocked_requesting_operation_name: str,
      mocked_state: mock.Mock,
  ) -> None:
    index = generate_result_index()

    instance = DefaultLookup(
        index,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )

    instance.apply(mocked_state)

    mocked_default_subclasses["NameLookup"].assert_not_called()

  def test_apply__result_name__applies_name_lookup(
      self,
      mocked_default_subclasses: Dict[str, mock.Mock],
      mocked_lookup_expression: mock.Mock,
      mocked_requesting_operation_name: str,
      mocked_state: mock.Mock,
  ) -> None:
    mock_name = generate_static_name()

    instance = DefaultLookup(
        LOOKUP_STATIC_VALUE_MARKER + mock_name,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )

    instance.apply(mocked_state)

    mocked_default_subclasses["NameLookup"].assert_called_once_with(
        LOOKUP_STATIC_VALUE_MARKER + mock_name,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )
    mocked_default_subclasses["NameLookup"].\
        return_value.apply.assert_called_once_with(mocked_state)

  def test_apply__result_name__does_not_apply_index_lookup(
      self,
      mocked_default_subclasses: Dict[str, mock.Mock],
      mocked_lookup_expression: mock.Mock,
      mocked_requesting_operation_name: str,
      mocked_state: mock.Mock,
  ) -> None:
    mock_name = generate_static_name()

    instance = DefaultLookup(
        LOOKUP_STATIC_VALUE_MARKER + mock_name,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )

    instance.apply(mocked_state)

    mocked_default_subclasses["IndexLookup"].assert_not_called()

  def test_apply__invalid_name__does_not_apply_index_lookup(
      self,
      mocked_default_subclasses: Dict[str, mock.Mock],
      mocked_lookup_expression: mock.Mock,
      mocked_requesting_operation_name: str,
      mocked_state: mock.Mock,
  ) -> None:
    mock_name = generate_static_name()

    instance = DefaultLookup(
        mock_name,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )

    with pytest.raises(LookupUnknown):
      instance.apply(mocked_state)

    mocked_default_subclasses["IndexLookup"].assert_not_called()

  def test_apply__invalid_name__does_not_apply_name_lookup(
      self,
      mocked_default_subclasses: Dict[str, mock.Mock],
      mocked_lookup_expression: mock.Mock,
      mocked_requesting_operation_name: str,
      mocked_state: mock.Mock,
  ) -> None:
    mock_name = generate_static_name()

    instance = DefaultLookup(
        mock_name,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )

    with pytest.raises(LookupUnknown):
      instance.apply(mocked_state)

    mocked_default_subclasses["NameLookup"].assert_not_called()

  def test_apply__invalid_name__raises_unknown_lookup(
      self,
      mocked_lookup_expression: mock.Mock,
      mocked_requesting_operation_name: str,
      mocked_state: mock.Mock,
  ) -> None:
    mock_name = generate_static_name()

    instance = DefaultLookup(
        mock_name,
        mocked_lookup_expression,
        mocked_requesting_operation_name,
    )

    with pytest.raises(LookupUnknown) as exc:
      instance.apply(mocked_state)

    assert_is_lookup_unknown(
        exc=exc,
        lookup=instance,
    )
