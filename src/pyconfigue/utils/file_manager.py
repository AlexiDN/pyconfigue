import hashlib
from typing import Any
from pyconfigue.utils.enum import FileType
import yaml
import toml
import json


class FileManager:
    def __init__(self, file_path: str) -> None:
        self.file_type = FileType.from_file_extension(file_path.split(".")[1])
        self.file_path = file_path
        self.file_hash = None

    def parse_file(self) -> dict[str, Any]:
        """Open the file, parse it and return the resulting object"""
        with open(self.file_path, encoding="utf-8") as stream:
            match self.file_type:
                case FileType.YAML:
                    content = yaml.safe_load(stream)
                case FileType.TOML:
                    content = toml.load(stream)
                case FileType.JSON:
                    content = json.load(stream)
            if not isinstance(content, dict) and all(isinstance(key, str) for key in content):
                msg = f"ConFigue file {self.file_path} data does not match type dict[str, Any]"
                raise TypeError(msg)
            return content

    def write_file(self, content: dict[str, Any]) -> None:
        """Write a dictionnary to the file at self.file_path"""
        with open(self.file_path, encoding="utf-8", mode="w") as stream:
            match self.file_type:
                case FileType.YAML:
                    yaml.safe_dump(content, stream)
                case FileType.TOML:
                    toml.dump(content, stream)
                case FileType.JSON:
                    json.dump(content, stream)

    def compute_file_hash(self, algorithm: str = "sha256") -> str:
        """Compute the hash of the file using the specified algorithm."""
        hash_func = hashlib.new(algorithm)

        with open(self.file_path, "rb") as file:
            # Read the file in chunks of 8192 bytes
            while chunk := file.read(8192):
                hash_func.update(chunk)

        return hash_func.hexdigest()

    def file_changed(self) -> bool:
        """Returned wether the file changed since last hash was computed"""
        if not self.file_hash:
            self.file_hash = self.compute_file_hash()
            return True
        return self.compute_file_hash() != self.file_hash
