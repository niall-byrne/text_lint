"""Test the ValidateDebug class."""

import json
from typing import List
from unittest import mock

from text_lint.__helpers__.operations import (
    AliasOperationAttributes,
    assert_operation_attributes,
    assert_operation_inheritance,
)
from text_lint.__helpers__.translations import assert_is_translated
from text_lint.operations.validators.args.result_set import ResultSetArg
from ..bases.validator_base import ValidationBase
from ..validate_debug import ValidateDebug


class TestValidateDebug:
  """Test the ValidateDebug class."""

  def test_initialize__defined__attributes(
      self,
      validate_debug_instance: ValidateDebug,
      mocked_validator_name: str,
  ) -> None:
    attributes: AliasOperationAttributes = {
        "hint": "output save id lookups to the console",
        "name": mocked_validator_name,
        "operation": "validate_debug",
    }

    assert_operation_attributes(
        validate_debug_instance,
        attributes,
    )

  def test_initialize__translations(
      self,
      validate_debug_instance: ValidateDebug,
  ) -> None:
    assert_is_translated(validate_debug_instance.hint)
    assert_is_translated(validate_debug_instance.msg_fmt_debug)

  def test_initialize__inheritance(
      self,
      validate_debug_instance: ValidateDebug,
  ) -> None:
    assert_operation_inheritance(
        validate_debug_instance,
        bases=(ValidationBase, ValidateDebug),
    )

  def test_initialize__creates_result_set_arg_instance(
      self,
      mocked_result_set: List[str],
      validate_debug_instance: ValidateDebug,
  ) -> None:
    assert isinstance(validate_debug_instance.saved_results, ResultSetArg)
    requested_results = list(validate_debug_instance.saved_results)
    assert requested_results[0].name == mocked_result_set[0]
    assert requested_results[1].name == mocked_result_set[1]

  def test_apply__valid_lookups__performs_each_expected_lookup(
      self,
      mocked_controller: mock.Mock,
      validate_debug_instance: ValidateDebug,
  ) -> None:
    validate_debug_instance.apply(mocked_controller)

    requested_results = list(validate_debug_instance.saved_results)
    assert mocked_controller.forest.lookup.mock_calls == [
        mock.call(
            mocked_controller,
            requested_results[0],
            validate_debug_instance.name,
        ),
        mock.call(
            mocked_controller,
            requested_results[1],
            validate_debug_instance.name,
        ),
    ]

  def test_apply__valid_lookups__logs_expected_lookup_results(
      self,
      mocked_controller: mock.Mock,
      mocked_result_set: List[str],
      validate_debug_instance: ValidateDebug,
  ) -> None:
    mocked_controller.forest.lookup.side_effect = ("result_0", "result_1")

    validate_debug_instance.apply(mocked_controller)

    assert mocked_controller.log.mock_calls == [
        call for call_group in [
            [
                mock.call(
                    ValidateDebug.msg_fmt_debug.format(mock_result),
                    indent=True,
                ),
                mock.call(
                    json.dumps(
                        "result_{0}".format(index),
                        indent=4,
                        default=str,
                    )
                ),
            ] for index, mock_result in enumerate(mocked_result_set)
        ] for call in call_group
    ]
