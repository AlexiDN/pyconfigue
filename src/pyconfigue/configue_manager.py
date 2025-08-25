from typing import Any, get_type_hints

from pydantic import BaseModel

from pyconfigue.base_config import ValidatorModel
from pyconfigue.base_config import ConFigueModel
from pyconfigue.utils.exceptions import SetupError
from .providers.base_providers import ConFigueProvider


class ConFigueManager:
    """Configuration Manager Class. Used to define your configuration objects"""

    providers: list[ConFigueProvider]
    __configue_model: type[ConFigueModel]

    def __init__(self, providers: list[ConFigueProvider]) -> None:
        model_validator = self._create_validator_class_from_parent()
        # init providers
        self.providers = providers
        for provider in self.providers:
            provider.set_model_validator(model_validator)

    def __getattribute__(self, name: str) -> Any:
        """Return the config key if name is uppercase else return the attribute of the class"""
        if name.isupper():
            # Search onto providers
            for provider in self.providers:
                value = provider.get(name)
                value_type = get_type_hints(self.__configue_model).get(name)
                if value:
                    return self._convert_value(value, value_type)
            msg = f"No configuration entry was found for the key {name}"
            raise KeyError(msg)
        # Case attribute name is not a config key
        return super().__getattribute__(name)

    @staticmethod
    def _convert_value(value: Any, desired_type: type) -> Any:
        """Convert a value to the type specified"""
        if not isinstance(value, desired_type):
            # convert to Pydantic model
            if issubclass(desired_type, BaseModel):
                return desired_type.model_validate()
            # other types
            return desired_type(value)
        return value

    def _create_validator_class_from_parent(self) -> ValidatorModel:
        """Creates a pydantic class from the parent ConFigueModel if there is one.
        It can later be used to properly validate the dicts representing the model_cls
        """
        for base in self.__class__.__mro__[1:]:  # Skip cls itself
            if issubclass(base, ConFigueModel):
                self.__configue_model = base
                # Get type hints
                annotations = get_type_hints(base)

                # Dynamically create Validator class
                return type(f"{base.__name__}Validator", (ValidatorModel, base), {"__annotations__": annotations})

        raise SetupError("Your class should both inherit from ConFigueManager and ConFigueModel")
