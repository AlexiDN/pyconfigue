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

    def test_dump_resolves_all_keys(cls):
        manager = cls.get_instance()
        dump = manager.dump()
        assert dump["TEST_CONFIG_KEY"] == "json"  # file provider wins over default
        assert dump["TEST_CONFIG_KEY_2"] == 20
        assert dump["TEST_CONFIG_KEY_3"] == ["10", "20"]

    def test_to_model_returns_validated_instance(cls):
        manager = cls.get_instance()
        model = manager.to_model()
        assert model.TEST_CONFIG_KEY == "json"
        assert model.TEST_CONFIG_KEY_2 == 20
        assert model.TEST_CONFIG_KEY_3 == ["10", "20"]

    def test_to_model_raises_on_missing_key(cls):
        manager = cls.get_instance()
        manager.providers = []  # no provider can resolve any key
        with pytest.raises(KeyError):
            manager.to_model()
