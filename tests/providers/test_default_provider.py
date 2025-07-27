# ruff: noqa
from os import environ

import pytest

from pyconfigue.providers import DefaultProvider
from ressources import DEFAULT_CONFIGUES, SELECTOR_KEY, ConFigue1Test, configue_selector

TEST_KEY = "TEST_CONFIG_KEY"
TEST_VALUE = ConFigue1Test.TEST_CONFIG_KEY


class TestDefaultProvider:
    @staticmethod
    def test_init_empty_dict():
        with pytest.raises(ValueError):
            DefaultProvider({})

    @staticmethod
    def test_init_no_selector():
        with pytest.raises(ValueError):
            DefaultProvider(DEFAULT_CONFIGUES)

    @staticmethod
    def test_load_single_configue():
        provider = DefaultProvider(DEFAULT_CONFIGUES["1"])
        assert provider._config == DEFAULT_CONFIGUES["1"]

    @staticmethod
    def test_load_selector_case_1():
        environ[SELECTOR_KEY] = "1"
        provider = DefaultProvider(DEFAULT_CONFIGUES, configue_selector)
        assert provider._config == DEFAULT_CONFIGUES["1"]
        environ.pop(SELECTOR_KEY, None)

    @staticmethod
    def test_load_selector_case_2():
        provider = DefaultProvider(DEFAULT_CONFIGUES, configue_selector)
        assert provider._config == DEFAULT_CONFIGUES["2"]

    @staticmethod
    def test_get():
        provider = DefaultProvider(ConFigue1Test())
        assert provider.get(TEST_KEY) == TEST_VALUE

    @staticmethod
    def test_get_none():
        provider = DefaultProvider(ConFigue1Test())
        assert provider.get("UNDEFINED_KEY") is None
