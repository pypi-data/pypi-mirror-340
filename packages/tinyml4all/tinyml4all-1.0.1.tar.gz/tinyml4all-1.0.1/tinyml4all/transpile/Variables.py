from typing import Any, List, Set

from tinyml4all.transpile.Variable import Variable


class Variables:
    """
    Handle many Variables
    """
    # todo: type hint ChainStep
    def __init__(self, steps: List[Any]):
        """
        Constructor
        :param steps:
        """
        self.steps = steps

    @property
    def inputs(self) -> List[Variable]:
        """
        Get input variables
        :return:
        """
        return [var for var in self.steps[0].input_dtypes if not var.is_reserved]

    @property
    def all(self) -> Set[Variable]:
        """
        Get all variables, in no particular order
        :return:
        """
        return set(
            [var for step in self.steps for var in step.input_dtypes if not var.is_reserved] +
            [var for step in self.steps for var in step.output_dtypes]
        )