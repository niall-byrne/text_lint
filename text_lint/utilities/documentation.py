"""Documentation utilities."""

import sys
from typing import List

white_list = ["TYPE_CHECKING"]

SPHINX_TABLE_DIRECTIVE_PREFIX = """\n
.. list-table::
   :class: tight-table
   :widths: 30 30
   :header-rows: 1

   * - Attribute
     - Description
"""


def document_module_attributes(
    module_name: str,
    descriptions: List[str],
) -> None:
  """Dynamically document module attributes.

  :param module_name: The name of the module to document attributes for.
  :param descriptions: A list of descriptions corresponding to each attribute.
  """
  module = sys.modules[module_name]

  if not isinstance(module.__doc__, str):
    module.__doc__ = ""

  module.__doc__ += SPHINX_TABLE_DIRECTIVE_PREFIX
  attribute_index = 0

  for attribute in dir(module):
    if attribute == attribute.upper() and attribute not in white_list:
      module.__doc__ += "   * - " + attribute + "\n"
      module.__doc__ += "     - " + descriptions[attribute_index] + "\n"
      attribute_index += 1
