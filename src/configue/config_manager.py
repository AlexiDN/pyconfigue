from typing import Any, get_type_hints
from .providers.base_providers import ConfigProvider


class ConfigManager:
    """Configuration Manager Class. Used to define your configuration objects

    NOTE: All your configuration objects need to be define in uppercase
    """

    providers: list[ConfigProvider]

    def __init__(self, providers: list[ConfigProvider]) -> None:
        self.providers = providers

    def __getattribute__(self, name: str) -> Any:
        """Return the config key if name is uppercase else return the attribute of the class"""
        if name.isupper():
            for provider in self.providers:
                value = provider.get(name)
                value_type = get_type_hints(self.__class__).get(name)
                if value:
                    # try to convert the value to the type used as annotation
                    if value_type and type(value) is not value_type:
                        return value_type(value)
                    return value
            msg = f"No config entry was found for the key {name}"
            raise KeyError(msg)

        return super().__getattribute__(name)
