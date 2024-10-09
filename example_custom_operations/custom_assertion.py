"""An example custom text_lint assertion."""

from text_lint.extend import AssertionBase, AssertionState

YAML_EXAMPLE = """

- name: a simple custom assertion example
  operation: assert_custom

"""


class CustomAssertion(AssertionBase):
  """An example custom text_lint assertion."""

  magic_string = "magic_string"

  hint = "fails if \"{0}\" is found in the file".format(magic_string)
  operation = "assert_custom"
  yaml_example = YAML_EXAMPLE

  def __init__(
      self,
      name: str,
  ) -> None:
    super().__init__(name=name, save=None, splits=None)

  def apply(self, state: "AssertionState") -> None:

    data = state.next()

    if data == self.magic_string:
      state.fail(expected="not to be \"{0}\"".format(self.magic_string))
    else:
      # Allow another assertion to process this line
      state.rewind()
