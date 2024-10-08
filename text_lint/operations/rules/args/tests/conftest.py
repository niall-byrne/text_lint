"""Test fixtures for the string split classes."""
from typing import List

import pytest
from ..split import Split


@pytest.fixture
def split_instances() -> List[Split]:
  split1 = Split(group=0)
  split2 = Split(group=1, separator="-")
  return [split1, split2]
