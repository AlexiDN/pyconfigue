from enum import Enum


class FileType(str, Enum):
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"

    @classmethod
    def from_file_extension(cls, file_extension: str) -> "FileType":
        """Return the FileType matching the file extension"""
        file_extension = file_extension.removeprefix(".")
        file_extension = "yaml" if file_extension == "yml" else file_extension
        return cls(file_extension)
