# PyConFigue



## Features

This library provides you an easy way to properly manage your python application configuration easily.

The key features are:

- Multiple configuration sources support using configuration providers
- Sources priority managment using a layer based model
- Typed configuration
- Autocomplete from IDEs
- Support of objects configurations using [Pydantic](https://docs.pydantic.dev/latest/)

## Installation

```bash
pip install pyconfigue
```

## Usage

### 1 - Define your ConFigue Model

```python
from pyconfigue import ConFigueModel
from pydantic import BaseModel

class MyPydanticModel(BaseModel):
    key1: dict[str, str]
    key2: float

class MyConFigueModel(ConFigueModel):
    CONFIG_KEY: str
    CONFIG_KEY_2: int
    CONFIG_KEY_3: list[str]
    CONFIG_KEY_4: MyPydanticModel
```

### 2 - Define your Providers

```python
from pyconfigue.providers import StaticFileProvider,EnvProvider,DefaultProvider

# File Provider


file_provider = StaticFileProvider( ["my_file.yaml","my_file_2.yaml"])

# Environment Provider
env_provider=EnvProvider()

# Default Provider
class DefaultConFigue(MyConFigueModel):
    CONFIG_KEY = "test_value"
    CONFIG_KEY_2= 2
    CONFIG_KEY_3 = ["1", "2"]
    CONFIG_KEY_4 = MyPydanticModel(key1={"k1": "1", "k2": "2"}, key2=1.2)

default_provider = DefaultProvider(DefaultConFigue())

```

### 3 - Define your ConFigue Manager

```python
from pyconfigue import ConFigueManager
class MyAppConFigueManager(ConFigueManager, MyConFigueModel):
    pass

CONFIG=MyAppConFigueManager([env_provider, file_provider, default_provider])
```

### 4 - Use your ConFigue

```python
from .app_config import CONFIG

print("CONFIG VALUE of CONFIG_KEY",CONFIG.CONFIG_KEY)
```

## Documentation

See our [wiki](https://github.com/AlexiDN/pyconfigue/wiki) if you need more details about how the project works.

## License 

The project is under the MIT License.

## Requirements

The project requires:
- python = ">=3.10"
- pydantic = "^2.11.4"
- pyyaml = "^6.0.2"
- toml = "^0.10.2"

## Project Status

> **NOTE** <br>
> The project is currently in development phase. If you have any remark or question feel free to open an Issue