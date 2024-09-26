"""SplitLookup class."""

from typing import TYPE_CHECKING, Optional, cast

from text_lint.config import LOOKUP_TRANSFORMATION_PREFIX
from text_lint.exceptions.lookups import LookupFailure
from text_lint.utilities.translations import _, f
from .bases.lookup_encoder_base import LookupEncoderBase
from .encoders.split import SplitEncoder

if TYPE_CHECKING:  # pragma: no cover
  from text_lint.linter.states import LookupState
  from text_lint.operations.lookups.bases.lookup_base import AliasLookupParams
  from text_lint.operations.validators.args.lookup_expression import (
      LookupExpression,
  )


YAML_EXAMPLE_COMPONENTS = (
    _("split lookup example"),
)
YAML_EXAMPLE = """

- name: {0}
  operation: validate_debug
  saved:
    - example.split()
    - example.split("-").to_group()

""".format(*YAML_EXAMPLE_COMPONENTS)


class SplitLookup(LookupEncoderBase):
  """SplitLookup operation for ResultForest instances."""

  encoder_class = SplitEncoder
  hint = _("split the values of a save id")
  operation = LOOKUP_TRANSFORMATION_PREFIX + "split"
  yaml_example = YAML_EXAMPLE

  msg_fmg_invalid_parameters = _("Invalid split lookup parameters!")

  def __init__(
      self,
      lookup_name: str,
      lookup_expression: "LookupExpression",
      lookup_params: "AliasLookupParams",
      requesting_operation_name: str,
  ) -> None:
    super().__init__(
        lookup_name,
        lookup_expression,
        lookup_params,
        requesting_operation_name,
    )
    self.seperator = self._parse_seperator()

  def validate_params(self) -> None:
    try:
      assert len(self.lookup_params) < 2
      if len(self.lookup_params) == 1:
        assert isinstance(self.lookup_params[0], str)
    except AssertionError as exc:
      raise LookupFailure(
          translated_description=f(
              self.msg_fmg_invalid_parameters,
              [],
              nl=1,
          ),
          lookup=self,
      ) from exc

  def _parse_seperator(self) -> Optional[str]:
    if self.lookup_params:
      return cast(str, self.lookup_params[0])
    return None

  def apply(
      self,
      state: "LookupState",
  ) -> None:
    """Split all values at current location and in the lookup results."""

    self.encoder_params = {"seperator": self.seperator}

    state.results = self.encode(state.results)
