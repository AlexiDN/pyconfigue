# ruff: noqa
from os import environ
from ConFigue.providers import EnvProvider

TEST_KEY = "TEST_CONFIG_KEY"
TEST_VALUE = "test"


class TestEnvProvider:
    @staticmethod
    def test_get():
        environ[TEST_KEY] = TEST_VALUE
        provider = EnvProvider()
        assert provider.get(TEST_KEY) == TEST_VALUE
        environ.pop(TEST_KEY, None)

    @staticmethod
    def test_get_none():
        provider = EnvProvider()
        assert provider.get(TEST_KEY) is None
