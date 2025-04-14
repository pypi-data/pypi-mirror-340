from copy import deepcopy
from typing import List

from tinyml4all.support.types import TemplateDef
from tinyml4all.tabular.ProcessingBlock import ProcessingBlock
from tinyml4all.time.continuous.classification import Chain
from tinyml4all.time.continuous.features import Window
from tinyml4all.transpile.Variables import Variables


class BinaryChain(Chain):
    """
    Episodic classification chain on binary data
    """
    def __init__(self, label: str, *steps):
        """
        Constructor
        """
        super().__init__(*[deepcopy(step) for step in steps])
        self.label = label

    @property
    def ovr_steps(self) -> List[ProcessingBlock]:
        """
        Get steps after the window (included)
        :return:
        """
        window_index = next(i for i, step in enumerate(self.steps) if isinstance(step, Window))

        return self.steps[window_index + 1:]

    def get_template(self) -> TemplateDef:
        """
        Get template
        :return:
        """
        return {
            "steps": self.ovr_steps,
            "window": next(step for step in self.steps if isinstance(step, Window))
        }
