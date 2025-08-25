from typing import Any, Callable
from pyconfigue.providers.base_providers import DynamicConFigueProvider
from pyconfigue.utils.file_manager import FileManager


class DynamicFileProvider(DynamicConFigueProvider):
    configs_path: str
    configue_file_selector: Callable | None
    config_memory: dict

    def __init__(
        self,
        files_paths: dict[Any, str] | list[str] | str,
        configue_file_selector: Callable | None = None,
    ) -> None:
        if not files_paths:
            msg = "DynamicFileProvider can't be initialized without at least one ConFigue file path."
            raise ValueError(msg)
        config_paths = configue_file_selector(files_paths) if configue_file_selector else files_paths
        if isinstance(config_paths, str):
            config_paths = [config_paths]
        if isinstance(config_paths, dict):
            config_paths = list(config_paths.values())
        self.file_managers = [FileManager(path) for path in config_paths]
        self.config_memory = {}

    def get(self, key: str) -> Any:
        """Return the value associated to key  into the config file or None"""
        any_file_changed = False
        for file_manager in self.file_managers:
            # if file changed since last_time process all the next file_managers to keep priority
            if any_file_changed or file_manager.file_changed():
                any_file_changed = True
                self.config_memory.update(file_manager.parse_file())
        return getattr(
            self.model_validator.model_validate(obj=self.config_memory, ignore_missing_fields=True), key, None
        )

    def set(self, key: str, value: Any) -> None:
        """Register the value associated to the key into the config"""
        if not isinstance(self.configs_path, str):
            msg = "DynamicFileProvider can't set a value associated to a key if multiple files where provided"
            raise TypeError(msg)
        file_manager = FileManager(self.configs_path)
        content = file_manager.parse_file()
        content[key] = value
        file_manager.write_file(content)
