from tinyml4all.configurations.ConfigurableAttribute import ConfigurableAttribute


class Text(ConfigurableAttribute):
    """
    Text value
    """
    def __init__(self, name: str, **kwargs):
        """
        Constructor
        :param name:
        """
        super().__init__(name, **kwargs)
        self.custom["type"] = "text"

