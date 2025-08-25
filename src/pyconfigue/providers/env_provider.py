from os import environ
from typing import Any

from .base_providers import DynamicConFigueProvider


class EnvProvider(DynamicConFigueProvider):
    @staticmethod
    def get(key: str) -> str | None:
        """Return the value associated to the key as str or None"""
        return environ.get(key, None)

    @staticmethod
    def set(key: str, value: Any) -> None:
        """Set the value associated to the key inside the environment"""
        environ[key] = str(value)
