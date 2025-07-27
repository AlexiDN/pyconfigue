# ruff: noqa
from os import environ
from ConFigue.providers import DefaultProvider, EnvProvider
from ressources import ConFigue1Test, ConfigueManagerTest
import pytest


class TestConFigueManager:
    def get_instance(cls) -> ConfigueManagerTest:
        default_provider = DefaultProvider(ConFigue1Test())
        env_provider = EnvProvider()
        return ConfigueManagerTest([env_provider, default_provider])

    def test_get_key_define_once(cls):
        manager = cls.get_instance()
        assert manager.TEST_CONFIG_KEY == ConFigue1Test.TEST_CONFIG_KEY

    def test_get_key_define_multiple_times(cls):
        manager = cls.get_instance()
        valeu_from_env = "test_value_from_env2"
        environ["TEST_CONFIG_KEY"] = valeu_from_env
        assert manager.TEST_CONFIG_KEY == valeu_from_env
        environ.pop("TEST_CONFIG_KEY", None)

    def test_get_key_undefined(cls):
        manager = cls.get_instance()
        with pytest.raises(KeyError):
            manager.TEST_UNDEFINED_KEY
