"""Test the documentation utilities."""

import sys
from typing import Dict
from unittest import mock

import pytest
from text_lint.utilities import documentation


class TestModuleAttributes:
  """Test the module attributes documentation automation."""

  mocked_module_name = "document_module_attributes_test"
  scenarios = pytest.mark.parametrize(
      "attributes,expected",
      (
          [
              {
                  "A": "First letter of the alphabet.",
                  "b": "Second letter of the alphabet.",
              },
              "   * - A\n     - First letter of the alphabet.\n",
          ],
          [
              {
                  "ALPHA": "First letter of the greek alphabet.",
                  "BETA": "Second letter of the greek alphabet.",
              },
              (
                  "   * - ALPHA\n     - First letter of the greek alphabet.\n"
                  "   * - BETA\n     - Second letter of the greek alphabet.\n"
              ),
          ],
      ),
      ids=["A", "ALPHA,BETA"],
  )

  @scenarios
  def test__existing__vary_module__vary_description__updates__doc__(
      self,
      mocked_module: mock.Mock,
      attributes: Dict[str, str],
      expected: str,
  ) -> None:
    existing_doc = "Existing docstring content."
    mocked_module.__doc__ = existing_doc
    for name, description in attributes.items():
      setattr(mocked_module, name, description)
    with mock.patch.dict(
        sys.modules,
        {self.mocked_module_name: mocked_module},
        clear=False,
    ):

      documentation.document_module_attributes(
          self.mocked_module_name,
          list(attributes.values()),
      )

    assert mocked_module.__doc__ == (
        existing_doc + documentation.SPHINX_TABLE_DIRECTIVE_PREFIX + expected
    )

  @scenarios
  def test__no_existing__vary_module__vary_description__updates__doc__(
      self,
      mocked_module: mock.Mock,
      attributes: Dict[str, str],
      expected: str,
  ) -> None:
    mocked_module.__doc__ = None
    for name, description in attributes.items():
      setattr(mocked_module, name, description)
    with mock.patch.dict(
        sys.modules,
        {self.mocked_module_name: mocked_module},
        clear=False,
    ):

      documentation.document_module_attributes(
          self.mocked_module_name,
          list(attributes.values()),
      )

    assert mocked_module.__doc__ == (
        documentation.SPHINX_TABLE_DIRECTIVE_PREFIX + expected
    )
