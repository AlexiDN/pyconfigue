# ruff: noqa
import os

from pydantic import BaseModel
import pytest
from pyconfigue.utils.file_manager import FileManager
from ressources import TEST_FILE_DIR, ConFigueFileTest


class TestConfig(BaseModel, ConFigueFileTest):
    pass


TEST_DATA = TestConfig().model_dump()


class TestFileManager:
    @pytest.mark.parametrize(
        "extension",
        [
            "json",
            "yml",
            "toml",
        ],
    )
    @staticmethod
    def test_parse_file(extension):
        file_path = TEST_FILE_DIR + f"/test_config.{extension}"
        parsed_file = FileManager(file_path).parse_file()
        assert parsed_file == TEST_DATA

    @pytest.mark.parametrize(
        "extension",
        [
            "json",
            "yml",
            "toml",
        ],
    )
    @staticmethod
    def test_write_file(extension):
        file_path = TEST_FILE_DIR + f"/temp.{extension}"
        manager = FileManager(file_path)
        manager.write_file(TEST_DATA)
        assert os.path.exists(file_path)
        assert manager.parse_file() == TEST_DATA
        os.remove(file_path)

    @staticmethod
    def test_compute_file_hash():
        file_path = TEST_FILE_DIR + f"/test_config.json"
        manager = FileManager(file_path)
        assert manager.compute_file_hash()=="92900742fef3a551a6c84eacfc7fceda6253f33a42a4ec54ba9d516bd1a07860"

    @staticmethod
    def test_file_changed():
        data=FileManager(TEST_FILE_DIR + f"/test_config.json").parse_file()
        file_path = TEST_FILE_DIR + f"/temp.json"
        manager = FileManager(file_path)
        manager.write_file(data)
        manager.file_hash=manager.compute_file_hash()
        # write same data to validate file did not changed
        manager.write_file(data)
        assert not manager.file_changed()
        manager.write_file({})
        assert manager.file_changed()
        manager.write_file(data)