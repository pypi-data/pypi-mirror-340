from typing import List

from tinyml4all.configurations.ConfigurableAttribute import ConfigurableAttribute
from tinyml4all.configurations.Configuration import Configuration
from tinyml4all.support import override
from tinyml4all.support.types import ArrayOfStrings


class Configurable:
    """
    Interface for configurable objects
    """
    def get_configuration(self) -> Configuration:
        """
        Get base configuration
        :return:
        """
        override(self)

    def get_configurables(self) -> List[ConfigurableAttribute]:
        """
        Get configurable options
        :return:
        """
        override(self)

    def configure_columns(self, columns: ArrayOfStrings):
        """
        Configure columns.
        Meant to be overridden.
        :param columns:
        :return:
        """
        pass

    def to_config(self) -> dict:
        """

        :return:
        """
        conf = self.get_configuration()
        attributes = self.get_configurables()

        return {
            "type": f"{self.__class__.__module__}.{self.__class__.__name__}",
            "info": {
                "title": conf.title,
                "description": conf.description
            },
            "attributes": [attr.to_json() for attr in attributes]
        }