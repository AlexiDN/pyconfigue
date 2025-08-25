# ruff: noqa
# TODO Add dynamic change test
from os import environ

import pytest

from pyconfigue.providers import DynamicFileProvider
from ressources import (
    TEST_FILE_DIR,
    ConFigueFileTest,
    ModelValidatorTest,
    PydanticModelTest,
    configue_selector,
    SELECTOR_KEY,
)

TEST_KEY = "TEST_CONFIG_KEY_4"
TEST_VALUE = ConFigueFileTest.TEST_CONFIG_KEY_4
TEST_VALUE2 = PydanticModelTest(key1={"k1": "0", "k2": "0"}, key2=0.0)

TEST_FILE1 = TEST_FILE_DIR + f"/test_config.yml"
TEST_FILE2 = TEST_FILE_DIR + f"/test_partial_config.yml"
FILES_CONFIGS = {"1": TEST_FILE1, "2": TEST_FILE2}


class TestDynamicFileProvider:
    @staticmethod
    def test_init_empty_dict():
        with pytest.raises(ValueError):
            DynamicFileProvider( {})

    @staticmethod
    def test_get_single_configue():
        provider = DynamicFileProvider(TEST_FILE1)
        provider.set_model_validator(ModelValidatorTest)
        assert provider.get(TEST_KEY) == TEST_VALUE

    @staticmethod
    def test_get_multiple_configue():
        provider = DynamicFileProvider( [TEST_FILE1, TEST_FILE2])
        provider.set_model_validator(ModelValidatorTest)
        assert provider.get(TEST_KEY) == TEST_VALUE2

    @staticmethod
    def test_get_multiple_configue_configue_selector():
        environ[SELECTOR_KEY] = "1"
        provider = DynamicFileProvider(
            FILES_CONFIGS,
            configue_file_selector=configue_selector,
        )
        provider.set_model_validator(ModelValidatorTest)
        assert provider.get(TEST_KEY) == TEST_VALUE
        environ.pop(TEST_KEY, None)

    @staticmethod
    def test_get_none():
        provider = DynamicFileProvider( TEST_FILE1)
        provider.set_model_validator(ModelValidatorTest)
        assert provider.get("UNDEFINED_KEY") is None
