from typing import Any, get_type_hints

from pydantic import BaseModel
from .providers.base_providers import ConfigProvider


class ConFigueManager:
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
                    return self._convert_value(value, value_type)
            msg = f"No configuration entry was found for the key {name}"
            raise KeyError(msg)

        return super().__getattribute__(name)

    @staticmethod
    def _convert_value(value: Any, desired_type: type) -> Any:
        """Convert a value to the type specified"""
        # convert to Pydantic model
        if issubclass(desired_type, BaseModel):
            return desired_type.model_validate()
        # other types
        return desired_type(value)
