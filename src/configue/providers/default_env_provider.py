from typing import Any
from .base_providers import StaticConfigProvider
from configue.base_config import BaseConfig


class DefaultProvider(StaticConfigProvider):
    def __init__(self, config: BaseConfig) -> None:
        super().__init__(config)

    def _load_config(self, config: BaseConfig) -> None:
        """Load the default config object"""
        self._config = config

    def get(self, key: str) -> Any:
        """Return the value associated to _config.<key> or None"""
        return getattr(self._config, key, None)
