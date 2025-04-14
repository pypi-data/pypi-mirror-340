from typing import List, Any


from tinyml4all.support.types import coalesce, TemplateDef
from tinyml4all.tabular.ProcessingBlock import ProcessingBlock
from tinyml4all.time.continuous.classification.ContinuousClassificationTimeSeries import \
    ContinuousClassificationTimeSeries
from tinyml4all.time.continuous.features.Window import Window as ContinuousWindow
from tinyml4all.time.continuous.classification import Chain as ContinuousChain
from tinyml4all.time.episodic.classification.BinaryChain import BinaryChain
from tinyml4all.time.episodic.classification.BinaryDataset import BinaryDataset
from tinyml4all.time.episodic.classification.EpisodicClassificationTimeSeries import EpisodicClassificationTimeSeries
from tinyml4all.time.episodic.features import Window
from tinyml4all.time.continuous.classification import Chain as Base
from tinyml4all.transpile.Variables import Variables


class Chain(Base):
    """
    Episodic time series classification chain
    """
    @staticmethod
    def hydrate(blocks: List[dict]) -> "Chain":
        """
        Hydrate chain from block objects
        :param blocks:
        :return:
        """
        # todo
        pass

    def __init__(self, *, window: Window, ovr: List[ProcessingBlock], pre: List[ProcessingBlock] = None):
        """
        Constructor
        :param window:
        :param ovr:
        :param pre:
        """
        Base.__init__(self)

        self.pre = coalesce(pre, [])
        self.window = window
        self.ovr = ovr
        self.chains : List[ContinuousChain] = []

    def get_template(self) -> TemplateDef:
        """
        Get template
        :return:
        """
        return {
            "variables": Variables([step for chain in self.chains for step in chain.steps]),
            "pre": self.pre,
            "window": sorted([chain.get_step_of_type(ContinuousWindow) for chain in self.chains], key=lambda window: window.length)[-1],
            "chains": self.chains
        }

    def fit(self, dataset: EpisodicClassificationTimeSeries, *args, **kwargs) -> List[ContinuousClassificationTimeSeries]:
        """
        Fit binary versions of the dataset
        :param dataset:
        :param args:
        :param kwargs:
        :return:
        """
        self.unfit()

        tables = []
        self.chains = []

        for i, label in enumerate(dataset.unique_labels):
            # convert episodic to binary continuous
            binary_dataset = BinaryDataset.convert(dataset, label=label)
            duration = dataset.event_durations[label]
            half = duration / 2

            for t in binary_dataset.event_timestamps:
                start_at = t - half - self.window.shift
                end_at = t + half + self.window.shift
                binary_dataset.add_label(label, start_at, end_at)

            # create continuous chain
            window = ContinuousWindow(length=duration, shift=self.window.shift, features=self.window.features)
            binary_chain = BinaryChain(label, *(self.pre + [window] + self.ovr))

            tables.append(binary_chain(binary_dataset))
            self.chains.append(binary_chain)

            # fit pre-processing steps once
            if i == 0 and len(self.pre) > 0:
                BinaryChain(label, *self.pre).fit(binary_dataset)

        self.fitted = True

        return tables

    def transform(self, dataset: EpisodicClassificationTimeSeries, *args, **kwargs) -> Any:
        """
        Transform dataset
        :param dataset:
        :param args:
        :param kwargs:
        :return:
        """
        results = []

        for chain in self.chains:
            binary_dataset = BinaryDataset.convert(dataset, label=chain.label)
            duration = dataset.event_durations[chain.label]
            half = duration / 2

            for t in binary_dataset.event_timestamps:
                start_at = t - half - self.window.shift
                end_at = t + half + self.window.shift
                binary_dataset.add_label(chain.label, start_at, end_at)

            results.append(chain(binary_dataset))

        return results

