"""Test the ResultTreeEncoder class."""
import json
from unittest import mock

from text_lint.results.tree import ResultTree
from ..tree import ResultTreeEncoder
from .conftest import AliasSetupEncoderMock


class TestResultTreeEncoder:
  """Test the ResultTreeEncoder class."""

  def test_initialize__inheritance(
      self,
      concrete_result_tree_encoder_instance: ResultTreeEncoder,
  ) -> None:
    assert isinstance(
        concrete_result_tree_encoder_instance,
        ResultTreeEncoder,
    )
    assert isinstance(
        concrete_result_tree_encoder_instance,
        json.JSONEncoder,
    )

  def test_encode__non_tree_value__pass_through(
      self,
      concrete_result_tree_encoder_instance: ResultTreeEncoder,
      setup_encoder_mock: AliasSetupEncoderMock,
  ) -> None:
    mocked_default_encoder = setup_encoder_mock(
        method="default", return_value=0
    )
    mocked_non_tree_object = mock.Mock()
    mocked_object = {
        "non-tree": mocked_non_tree_object,
        "nested": {
            "object": "HERE"
        },
    }

    return_value = concrete_result_tree_encoder_instance.encode(mocked_object)

    mocked_default_encoder.assert_called_once_with(mocked_non_tree_object)
    assert return_value == json.dumps(
        {
            "non-tree": mocked_non_tree_object,
            "nested": {
                "object": "HERE"
            }
        }
    )

  def test_encode__converts_result_tree_as_expected(
      self,
      concrete_result_tree_encoder_instance: ResultTreeEncoder,
  ) -> None:
    mocked_result_tree = mock.Mock(spec=ResultTree)
    mocked_result_tree.representation.return_value = "mocked_representation"
    mocked_object = {
        "tree": mocked_result_tree,
        "nested": {
            "object": "HERE"
        },
    }

    return_value = concrete_result_tree_encoder_instance.encode(mocked_object)

    assert return_value == json.dumps(
        {
            "tree": mocked_result_tree.representation.return_value,
            "nested": {
                "object": "HERE"
            }
        }
    )
