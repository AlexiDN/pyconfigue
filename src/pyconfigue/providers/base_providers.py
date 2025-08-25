from abc import abstractmethod
from typing import Any

from pyconfigue.base_config import ValidatorModel


class ConFigueProvider:
    """The base provider class"""

    model_validator: ValidatorModel

    @abstractmethod
    def get(self, key: str) -> Any | None:
        """Return the value associated to the key or None"""

    def set_model_validator(self, model: ValidatorModel) -> None:
        """Setter for model"""
        self.model_validator = model


class StaticConFigueProvider(ConFigueProvider):
    """Provider for static configurations
    It load the configuration during construction use it after
    """

    _config: object = None

    @abstractmethod
    def load_config(self) -> None:
        """Load the static configuration within the object"""

    def get(self, key: str) -> Any:
        """Return the value associated to _config.<key> or None"""
        if not self._config:
            self.load_config()
        return getattr(self._config, key, None)


class DynamicConFigueProvider(ConFigueProvider):
    """Provider for dynamic configurations
    It load the value associated to a key when it is requested
    """

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Update the value associated to the key"""
