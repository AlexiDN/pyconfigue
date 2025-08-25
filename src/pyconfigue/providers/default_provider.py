from typing import Any, Callable
from .base_providers import StaticConFigueProvider
from pyconfigue.base_config import ConFigueModel


class DefaultProvider(StaticConFigueProvider):
    configue_selector: Callable | None

    def __init__(
        self, configues: dict[Any, ConFigueModel] | ConFigueModel, configue_selector: Callable | None = None
    ) -> None:
        if not configues:
            msg = "DefaultProvider can't be initialized without at least one ConFigueModel"
            raise ValueError(msg)
        if not configue_selector and isinstance(configues, dict):
            msg = (
                "DefaultProvider require configue_selector to be defined if multiple ConFigueModel objects are provided"
            )
            raise ValueError(msg)
        self.configue_selector = configue_selector
        self.configues = configues

    def load_config(self) -> None:
        """Load the default ConFigueModel object"""
        self._config = self.configue_selector(self.configues) if self.configue_selector else self.configues
