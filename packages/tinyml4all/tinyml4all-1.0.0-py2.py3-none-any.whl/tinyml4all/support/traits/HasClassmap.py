from typing import Dict, List

from tinyml4all.support import non_null


class HasClassmap:
    """
    Mixin for classes that have a classmap
    """
    @property
    def unique_labels(self) -> List[str]:
        """
        Get unique labels
        :return:
        """
        return sorted(non_null(set(self.Y_true)))

    @property
    def classmap(self) -> Dict[str, int]:
        """
        Get mapping from label to index
        :return:
        """
        return {str(y): i for i, y in enumerate(self.unique_labels)}

    @property
    def inverse_classmap(self) -> Dict[int, str]:
        """
        Get mapping from label to index
        :return:
        """
        return {i: str(y) for i, y in enumerate(self.unique_labels)}