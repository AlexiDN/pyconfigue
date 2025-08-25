# Changelog

## [0.0.1] - 2025-08

### Added*

- DynamicFileProvider and StaticFileProvider to manage configurations from files.
    - Support the following extensions: yaml/yml,toml and json.
    - Support multiple files per Provider
- ConFigueValidationModel to validate configurations from files using Pydantic Model validation

### Changed

- StaticConfigProvider and DynamicConfigProvider base classes.
    - Those became StaticConFigueProvider and DynamicConFigueProvider to match the lib universe.
- ConFigue is now ConFigueModel

## [0.0.1a0] - 2025-07

### Added

- EnvProvider to manage configurations defined by environment variables.
- DefaultProvider to manage default configurations.
- StaticConfigProvider and DynamicConfigProvider base classes.
- ConFigue base class to define ConFigue Model