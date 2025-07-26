from os import environ

from .base_providers import DynamicConfigProvider


class EnvironmentConfigProvider(DynamicConfigProvider):
    @staticmethod
    def get(key: str) -> str | None:
        """Return the value associated to the key as str or None"""
        return environ.get(key, None)
