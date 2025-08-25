# ruff: noqa
from os import environ
from pathlib import Path
from typing import Any
from pydantic import BaseModel
from pyconfigue import ConFigueModel
from pyconfigue.base_config import ValidatorModel
from pyconfigue.configue_manager import ConFigueManager

TEST_FILE_DIR = str(Path(__file__).parent.joinpath("tests_files"))


class PydanticModelTest(BaseModel):
    key1: dict[str, str]
    key2: float


class ConFigueModelTest(ConFigueModel):
    TEST_CONFIG_KEY: str
    TEST_CONFIG_KEY_2: int
    TEST_CONFIG_KEY_3: list[str]
    TEST_CONFIG_KEY_4: PydanticModelTest

class ModelValidatorTest(ConFigueModelTest,ValidatorModel):
    pass

class ConFigue1Test(ConFigueModelTest):
    TEST_CONFIG_KEY: str = "test_value"
    TEST_CONFIG_KEY_2: int = 2
    TEST_CONFIG_KEY_3: list[str] = ["1", "2"]
    TEST_CONFIG_KEY_4: PydanticModelTest = PydanticModelTest(key1={"k1": "1", "k2": "2"}, key2=1.2)


class ConFigue2Test(ConFigueModelTest):
    TEST_CONFIG_KEY: str = "test_value2"
    TEST_CONFIG_KEY_2: int = 3
    TEST_CONFIG_KEY_3: list[str] = []
    TEST_CONFIG_KEY_4: PydanticModelTest = PydanticModelTest(key1={"k1": "t"}, key2=5.0)


class ConFigueFileTest(ConFigueModelTest):
    TEST_CONFIG_KEY: str = "json"
    TEST_CONFIG_KEY_2: int = 20
    TEST_CONFIG_KEY_3: list[str] = ["10", "20"]
    TEST_CONFIG_KEY_4: PydanticModelTest = PydanticModelTest(key1={"k1": "k1", "k2": "k2"}, key2=5.0)

class ConfigueManagerTest(ConFigueManager, ConFigueModelTest):
    pass


SELECTOR_KEY = "TEST_CONFIGUE"
DEFAULT_CONFIGUES = {"1": ConFigue1Test(), "2": ConFigue2Test()}


def configue_selector(configues: dict[str, Any]) -> Any:
    """Select the ConFigue object based on env variable"""
    return configues.get(environ.get(SELECTOR_KEY, "2"))
