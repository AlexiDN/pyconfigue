from abc import abstractmethod
from typing import Any


class ConfigProvider:
    """The base provider class"""

    @abstractmethod
    def get(self, key: str) -> Any | None:
        """Return the value associated to the key or None"""


class StaticConfigProvider(ConfigProvider):
    """Provider for static configurations
    It load the configuration during construction use it after
    """

    _config: dict[str, Any]

    def __init__(self, *args: tuple | list, **kwargs: dict[str, Any]) -> None:
        self._config = {}
        self._load_config(*args, **kwargs)

    @abstractmethod
    def _load_config(self, *args: tuple | list, **kwargs: dict[str, Any]) -> None:
        """Load the static configuration within the object"""

    def get(self, key: str) -> Any | None:
        """Return the value associated to the key in _config or None"""
        return self._config.get(key)


class DynamicConfigProvider(ConfigProvider):
    """Provider for dynamic configurations
    It load the value associated to a key when it is requested
    """
