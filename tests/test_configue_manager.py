# ruff: noqa
from os import environ
from pyconfigue.providers import DefaultProvider, EnvProvider, DynamicFileProvider
from ressources import TEST_FILE_DIR, ConFigue1Test,ConFigueModelTest,ConfigueManagerTest
import pytest


class TestConFigueManager:
    def get_instance(cls) -> ConfigueManagerTest:
        default_provider = DefaultProvider(ConFigue1Test())
        env_provider = EnvProvider()
        file_provider = DynamicFileProvider( TEST_FILE_DIR + f"/test_config.yml")
        
        return ConfigueManagerTest(providers=[env_provider, file_provider, default_provider])

    def test_get_key_define_once(cls):
        manager = cls.get_instance()
        manager.providers.pop(1)  # remove file provider
        assert manager.TEST_CONFIG_KEY == ConFigue1Test().TEST_CONFIG_KEY

    def test_get_key_define_multiple_times(cls):
        manager = cls.get_instance()
        # key define by env provider
        assert manager.TEST_CONFIG_KEY != ConFigue1Test().TEST_CONFIG_KEY
        assert manager.TEST_CONFIG_KEY == "json"
        # define key in env
        value_from_env = "test_value_from_env2"
        environ["TEST_CONFIG_KEY"] = value_from_env
        assert manager.TEST_CONFIG_KEY == value_from_env
        environ.pop("TEST_CONFIG_KEY", None)

    def test_get_key_undefined(cls):
        manager = cls.get_instance()
        with pytest.raises(KeyError):
            manager.TEST_UNDEFINED_KEY
