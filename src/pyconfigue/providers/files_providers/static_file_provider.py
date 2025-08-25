from typing import Any, Callable

from pyconfigue.utils.file_manager import FileManager
from pyconfigue.providers.base_providers import StaticConFigueProvider


class StaticFileProvider(StaticConFigueProvider):
    configue_file_selector: Callable | None

    def __init__(
        self,
        files_paths: dict[Any, str] | list[str] | str,
        configue_file_selector: Callable | None = None,
    ) -> None:
        if not files_paths:
            msg = "StaticFileProvider can't be initialized without at least one ConFigue file path."
            raise ValueError(msg)
        self.configue_file_selector = configue_file_selector
        self.files_paths = files_paths

    def load_config(
        self,
    ) -> None:
        """Load the ConFigue object from file"""
        config_paths = (
            self.configue_file_selector(self.files_paths) if self.configue_file_selector else self.files_paths
        )
        if isinstance(config_paths, str):
            config_paths = [config_paths]
        if isinstance(config_paths, dict):
            config_paths = list(config_paths.values())
        content = {}
        for path in config_paths:
            content.update(FileManager(path).parse_file())
        self._config = self.model_validator.model_validate(obj=content, ignore_missing_fields=True)
