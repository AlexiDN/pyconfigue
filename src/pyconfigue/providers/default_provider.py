from typing import Any, Callable
from .base_providers import StaticConfigProvider
from pyconfigue.base_config import ConFigue


class DefaultProvider(StaticConfigProvider):
    configue_selector: Callable | None

    def __init__(self, configues: dict[Any, ConFigue] | ConFigue, configue_selector: Callable | None = None) -> None:
        if not configues:
            msg = "DefaultProvider can't be initialized without at least one ConFigue"
            raise ValueError(msg)
        if not configue_selector and isinstance(configues, dict):
            msg = "DefaultProvider require configue_selector to be defined if multiple ConFigue objects are provided"
            raise ValueError(msg)
        self.configue_selector = configue_selector
        super().__init__(configues)

    def _load_config(self, configues: dict[Any, ConFigue] | ConFigue) -> None:
        """Load the default ConFigue object"""
        self._config = self.configue_selector(configues) if self.configue_selector else configues

    def get(self, key: str) -> Any:
        """Return the value associated to _config.<key> or None"""
        return getattr(self._config, key, None)
